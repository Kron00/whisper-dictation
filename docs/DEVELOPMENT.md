# Development Guide

Contributing to Whisper Dictation - architecture, components, and development workflow.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Component Details](#component-details)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Adding Features](#adding-features)
- [Research Documentation](#research-documentation)
- [Contributing](#contributing)

## Architecture Overview

Whisper Dictation uses a daemon-based architecture for instant transcription:

```
┌─────────────────┐
│  whisper-hotkey │  ← Listens for double middle-click
│   (evdev loop)  │
└────────┬────────┘
         │ detects click
         ↓
┌─────────────────┐
│ whisper-dictate │  ← Orchestrates recording & transcription
│  (bash script)  │
└────────┬────────┘
         │ records audio (pw-record)
         │ sends to daemon via socket
         ↓
┌─────────────────┐
│  whisper-daemon │  ← Keeps model hot in VRAM
│ (Python+NeMo)   │  ← Transcribes instantly
└────────┬────────┘
         │ returns text
         ↓
┌─────────────────┐
│  whisper-flow   │  ← Optional LLM processing
│  (Python+LLM)   │
└────────┬────────┘
         │ polished text
         ↓
┌─────────────────┐
│  Clipboard +    │  ← Paste via ydotool
│  Keyboard       │
└─────────────────┘
```

### Key Design Decisions

1. **Daemon architecture**: Keep model loaded in VRAM for instant transcription
2. **Unix sockets**: Fast IPC between components
3. **Systemd services**: Automatic startup, restart on failure
4. **Bash orchestration**: Simple, reliable, easy to modify
5. **Modular design**: Each component is independent and replaceable

## Component Details

### whisper-daemon (Python)

**Purpose**: Keeps Parakeet model loaded in VRAM for instant transcription.

**Key Features**:
- Loads model on startup (~30 seconds)
- Listens on Unix socket `/tmp/whisper-daemon.sock`
- Processes audio files sent via socket
- Applies filler word removal
- Converts spoken punctuation to symbols
- Tracks statistics in SQLite database

**IPC Protocol**:
```python
# Client sends JSON:
{"audio_path": "/path/to/file.wav"}

# Daemon responds with JSON:
{"text": "transcribed text here", "language": "en"}
```

**Status File**: `/tmp/whisper-daemon.status`
- `starting` - Model loading
- `ready` - Ready for transcription
- `error: <message>` - Error state

**Key Functions**:
- `load_model()` - Initialize Parakeet model
- `transcribe_audio()` - Process audio file
- `remove_filler_words()` - Clean up text
- `process_punctuation()` - Convert spoken punctuation

### whisper-hotkey (Python)

**Purpose**: Detect double middle-click to trigger recording.

**Key Features**:
- Uses evdev to read mouse events directly
- Configurable double-click threshold
- Looks for specific mouse device pattern
- Toggles recording state via whisper-mode

**State Management**:
```python
IDLE → (first click) → WAITING → (second click within threshold) → RECORD
                    → (timeout) → IDLE
```

**Key Functions**:
- `find_mouse_device()` - Locate mouse in /dev/input
- `detect_double_click()` - Track click timing
- `toggle_recording()` - Start/stop via whisper-mode

### whisper-dictate (Bash)

**Purpose**: Orchestrate the recording and transcription process.

**Workflow**:
1. Check recording state (file lock)
2. Play start sound
3. Auto-pause music (playerctl)
4. Record audio via pw-record (PipeWire)
5. Play stop sound
6. Send audio to daemon via socket
7. Receive transcribed text
8. Optional: Send through flow mode (LLM)
9. Copy to clipboard (wl-copy)
10. Paste via ydotool (Ctrl+Shift+V)
11. Resume music

**State Files**:
- `/tmp/whisper-recording.lock` - Recording in progress
- `/tmp/whisper-daemon.sock` - Daemon socket
- `/tmp/recording.wav` - Temporary audio file

### whisperstats (Python + GTK4)

**Purpose**: Display usage statistics in a graphical dashboard.

**Features**:
- Shows words dictated (today/all-time)
- Calculates time saved vs typing
- Displays average speaking rate (WPM)
- Lists recent dictations
- Shows language detection stats

**Database Schema**:
```sql
CREATE TABLE dictations (
    id INTEGER PRIMARY KEY,
    timestamp TEXT,
    text TEXT,
    word_count INTEGER,
    duration_seconds REAL,
    language TEXT
);
```

### whisper-autogain (Python)

**Purpose**: Automatically adjust microphone gain for optimal levels.

**Learning Mode**:
1. Analyzes recent recordings
2. Calculates optimal gain level
3. Stores in `~/.config/whisper-dictation/autogain.json`
4. Applies before each recording

**Key Features**:
- Volume analysis of recorded audio
- Automatic gain adjustment via pactl
- Learns from usage patterns
- Stores/restores previous volume

### whisper-mode (Bash)

**Purpose**: Toggle between direct and flow modes.

**Modes**:
- `direct` - Paste transcription immediately
- `flow` - Send through LLM first

**State File**: `/tmp/whisper-mode.state`

### whisper-flow (Python)

**Purpose**: Process transcribed text through an LLM for grammar correction.

**Supported Backends**:
- Ollama (local LLMs)
- OpenAI API
- Any OpenAI-compatible endpoint

**Default Prompt**:
```
Fix grammar, punctuation, and formatting.
Keep the meaning intact. Return only the corrected text.
```

## Development Setup

### 1. Clone and Install

```bash
git clone https://github.com/Kron00/whisper-dictation.git
cd whisper-dictation
./install.sh
```

### 2. Development Workflow

**Edit scripts directly**:
```bash
# Scripts are in ~/.local/bin/
vim ~/.local/bin/whisper-daemon
vim ~/.local/bin/whisper-dictate
```

**Restart services after changes**:
```bash
systemctl --user restart whisper-daemon
systemctl --user restart whisper-hotkey
```

**View logs in real-time**:
```bash
journalctl --user -u whisper-daemon -f
journalctl --user -u whisper-hotkey -f
```

### 3. Testing Changes

**Test daemon manually**:
```bash
# Stop service
systemctl --user stop whisper-daemon

# Run manually to see output
~/.local/share/whisper-dictation/bin/python ~/.local/bin/whisper-daemon
```

**Test transcription**:
```bash
# Record a test file
pw-record test.wav
# (speak, then Ctrl+C)

# Send to daemon
echo '{"audio_path": "'$(pwd)'/test.wav"}' | nc -U /tmp/whisper-daemon.sock
```

## Code Style

### Python

- **PEP 8** compliance
- Type hints where helpful (not required for all code)
- Docstrings for non-obvious functions
- Error handling with try/except
- Logging instead of print() for services

**Example**:
```python
def transcribe_audio(audio_path: str) -> dict:
    """Transcribe audio file and return result.

    Args:
        audio_path: Path to WAV file

    Returns:
        dict with 'text' and 'language' keys
    """
    try:
        result = model.transcribe(audio_path)
        return {"text": result, "language": "en"}
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        return {"text": "", "language": "unknown"}
```

### Bash

- Use `shellcheck` to verify scripts
- Quote all variables: `"$variable"`
- Use `set -euo pipefail` at script start
- Comment non-obvious sections
- Prefer clarity over cleverness

**Example**:
```bash
#!/usr/bin/env bash
set -euo pipefail

# Record audio from default microphone
record_audio() {
    local output_file="$1"
    pw-record --format=s16 --rate=16000 "$output_file"
}
```

## Testing

### Unit Testing

Currently, the project doesn't have automated tests. Contributions welcome!

**Proposed structure**:
```
tests/
├── test_daemon.py        # Test daemon functions
├── test_punctuation.py   # Test punctuation processing
├── test_filler_words.py  # Test filler word removal
└── test_integration.py   # End-to-end tests
```

### Manual Testing

**Test checklist**:
- [ ] Double-click detection works
- [ ] Recording starts on first click
- [ ] Recording stops on second click
- [ ] Audio is recorded correctly
- [ ] Transcription is accurate
- [ ] Punctuation commands work
- [ ] Filler words are removed
- [ ] Text is pasted correctly
- [ ] Statistics are updated
- [ ] Services restart on failure

## Adding Features

### Example: Add a New Punctuation Command

1. **Edit the daemon** (`~/.local/bin/whisper-daemon`):

```python
PUNCTUATION_COMMANDS = [
    # ... existing commands ...
    (re.compile(r'\b(at symbol)\b', re.IGNORECASE), '@'),
]
```

2. **Test it**:
```bash
systemctl --user restart whisper-daemon
# Record: "hello at symbol example dot com"
# Should produce: "hello@example.com"
```

3. **Update documentation** (README.md):
Add to the punctuation table.

4. **Commit and PR**:
```bash
git checkout -b feature/at-symbol-command
git commit -am "Add 'at symbol' punctuation command"
git push origin feature/at-symbol-command
```

### Example: Add a New Statistics Metric

1. **Update database schema** in `whisper-daemon`:

```python
# In init_db():
cursor.execute('''
    ALTER TABLE dictations ADD COLUMN accuracy_score REAL
''')
```

2. **Track the metric** when saving stats:

```python
def update_stats(text, duration, language, accuracy):
    # ... existing code ...
    cursor.execute('''INSERT INTO dictations VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (None, timestamp, text, words, duration, language, accuracy))
```

3. **Display in WhisperStats**:

Update `whisperstats` to show the new metric.

## Research Documentation

The `research/` folder contains comprehensive documentation of design decisions:

- **spoken-punctuation/** - How spoken punctuation commands are implemented
- **voice-dictation-features/** - Analysis of features in commercial dictation software
- **whisper-stt-models-2025/** - Comparison of STT models and why Parakeet was chosen

When adding features, consider documenting:
- Why this approach was chosen
- What alternatives were considered
- Benchmarks or performance data
- Implementation examples

## Contributing

### Process

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/my-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Update documentation** if needed
6. **Commit with clear messages**: `git commit -am "Add feature X"`
7. **Push**: `git push origin feature/my-feature`
8. **Open a Pull Request** on GitHub

### Commit Messages

Use clear, descriptive commit messages:

```
Add noise reduction toggle feature

- Add whisper-noise script to toggle noise reduction
- Update daemon to check for noise reduction flag
- Add documentation to CONFIGURATION.md
```

### Code Review

PRs will be reviewed for:
- Code quality and style
- Test coverage (if applicable)
- Documentation updates
- Breaking changes (should be avoided)

### Areas for Contribution

**High Priority**:
- Automated testing
- CPU fallback mode (for non-NVIDIA GPUs)
- Support for additional mouse/keyboard combos
- Packaging (RPM, DEB, AUR)

**Medium Priority**:
- Web-based configuration UI
- Multi-language support
- Alternative STT models
- Performance optimizations

**Low Priority**:
- Docker containerization
- VSCode integration
- Custom hotkey configuration

## Architecture Improvements

Future architectural improvements to consider:

1. **Plugin system** - Allow custom post-processing plugins
2. **Config file** - Move hardcoded values to a config file
3. **D-Bus interface** - Standard Linux IPC for desktop integration
4. **Multiple models** - Support swapping between STT models
5. **Cloud sync** - Optional statistics sync across devices

## Questions?

- Open an issue on GitHub
- Check existing issues for similar questions
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common problems
