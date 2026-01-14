# Configuration Guide

Customize Whisper Dictation to your preferences.

## Table of Contents

- [Sound Effects](#sound-effects)
- [Double-Click Sensitivity](#double-click-sensitivity)
- [Filler Word Removal](#filler-word-removal)
- [Punctuation Commands](#punctuation-commands)
- [Noise Reduction](#noise-reduction)
- [Auto-Gain Microphone](#auto-gain-microphone)
- [Flow Mode (LLM Processing)](#flow-mode-llm-processing)
- [Mouse Device Configuration](#mouse-device-configuration)
- [Keyboard Shortcuts](#keyboard-shortcuts)

## Sound Effects

Whisper Dictation plays beep sounds when recording starts/stops. You can customize or disable these.

### Change Sound Files

Edit `~/.local/bin/whisper-dictate`:

```bash
# Default sounds
SOUND_START="/usr/share/sounds/freedesktop/stereo/message.oga"
SOUND_STOP="/usr/share/sounds/freedesktop/stereo/complete.oga"
```

Replace with your own sound files:

```bash
SOUND_START="/path/to/your/start.oga"
SOUND_STOP="/path/to/your/stop.oga"
```

### Disable Sounds

Comment out the sound lines:

```bash
# paplay "$SOUND_START" &
```

Or replace with silent commands:

```bash
SOUND_START="/dev/null"
SOUND_STOP="/dev/null"
```

## Double-Click Sensitivity

Adjust how fast you need to double-click to trigger recording.

Edit `~/.local/bin/whisper-hotkey`:

```python
DOUBLE_CLICK_THRESHOLD = 0.3  # seconds
```

- **Increase** (e.g., `0.5`) for slower double-clicks
- **Decrease** (e.g., `0.2`) for faster double-clicks

Restart the service after changes:

```bash
systemctl --user restart whisper-hotkey
```

## Filler Word Removal

The daemon automatically removes common filler words like "um", "uh", "like", etc.

### Customize Filler Words

Edit `~/.local/bin/whisper-daemon`:

```python
FILLER_PATTERNS = [
    re.compile(r'\b(um+|uh+|er+|ah+|hmm+)\b', re.IGNORECASE),
    re.compile(r'\b(you know)\b', re.IGNORECASE),
    re.compile(r'\b(basically|actually|literally)\b', re.IGNORECASE),
    re.compile(r'\b(i mean)\b', re.IGNORECASE),
    re.compile(r'\bso,\s', re.IGNORECASE),
    re.compile(r'\b(like,)\s', re.IGNORECASE),
]
```

Add your own patterns or remove existing ones.

### Disable Filler Word Removal

Comment out the entire `remove_filler_words()` function call in the daemon.

Restart after changes:

```bash
systemctl --user restart whisper-daemon
```

## Punctuation Commands

Spoken punctuation commands are processed by the daemon.

### Available Commands

See the main README for the full list. Default commands include:

- "period" → .
- "comma" → ,
- "question mark" → ?
- "exclamation point" → !
- "new line" → \\n
- "new paragraph" → \\n\\n
- etc.

### Customize Punctuation Commands

Edit `~/.local/bin/whisper-daemon`:

```python
PUNCTUATION_COMMANDS = [
    (re.compile(r'\b(exclamation point|exclamation mark)\b', re.IGNORECASE), '!'),
    (re.compile(r'\bperiod\b', re.IGNORECASE), '.'),
    (re.compile(r'\bcomma\b', re.IGNORECASE), ','),
    # Add your own:
    (re.compile(r'\bdash\b', re.IGNORECASE), ' - '),
]
```

**Note**: Longer phrases must come first in the list to match correctly.

Restart after changes:

```bash
systemctl --user restart whisper-daemon
```

## Noise Reduction

Enable background noise reduction for better transcription in noisy environments.

### Enable Noise Reduction

```bash
touch /tmp/whisper-noise-reduction.enabled
```

### Disable Noise Reduction

```bash
rm /tmp/whisper-noise-reduction.enabled
```

### Requirements

Noise reduction requires additional packages:

```bash
~/.local/share/whisper-dictation/bin/pip install noisereduce soundfile numpy
```

**Note**: Noise reduction adds ~0.5-1 second processing time per transcription.

## Auto-Gain Microphone

Auto-gain automatically adjusts your microphone volume for optimal recording levels.

### Enable Auto-Gain Learning

The system learns your optimal microphone volume over time:

```bash
whisper-autogain learn
```

This will:
- Analyze your recordings
- Automatically adjust microphone gain
- Store learned settings in `~/.config/whisper-dictation/autogain.json`

### Disable Auto-Gain

```bash
whisper-autogain disable
```

### Check Current Gain

```bash
whisper-autogain status
```

### Manual Gain Adjustment

You can also set a fixed gain level:

```bash
pactl set-source-volume @DEFAULT_SOURCE@ 80%
```

## Flow Mode (LLM Processing)

Flow mode sends transcribed text through an LLM for grammar correction and formatting.

### Enable Flow Mode

```bash
whisper-mode flow
```

### Disable Flow Mode

```bash
whisper-mode direct
```

### Configure LLM

Edit `~/.local/bin/whisper-flow.py` to configure your LLM endpoint:

```python
LLM_ENDPOINT = "http://localhost:11434/api/generate"  # Ollama default
MODEL = "llama2"
```

Supported backends:
- Ollama (local)
- OpenAI API
- Any OpenAI-compatible endpoint

### Custom Prompts

Modify the system prompt in `whisper-flow.py`:

```python
SYSTEM_PROMPT = """Fix grammar, punctuation, and formatting.
Keep the meaning intact. Return only the corrected text."""
```

## Mouse Device Configuration

By default, the hotkey listener looks for "Logitech USB Receiver". If you have a different mouse, you'll need to change this.

### Find Your Mouse Device

```bash
ls /dev/input/by-id/
```

Look for your mouse in the output (e.g., `usb-Logitech_USB_Receiver-event-mouse`).

### Configure Device

Edit `~/.local/bin/whisper-hotkey`:

```python
DEVICE_PATTERN = "Logitech USB Receiver"
```

Change to match your mouse name (partial match works):

```python
DEVICE_PATTERN = "Your Mouse Name"
```

Restart the service:

```bash
systemctl --user restart whisper-hotkey
```

## Keyboard Shortcuts

By default, transcribed text is pasted using **Ctrl+Shift+V** (plain text paste).

### Change Paste Shortcut

Edit `~/.local/bin/whisper-dictate`:

```bash
# Find the ydotool command (near the end)
echo "$final_text" | wl-copy
ydotool key 29:1 42:1 47:1 47:0 42:0 29:0  # Ctrl+Shift+V
```

Change to Ctrl+V (formatted paste):

```bash
ydotool key 29:1 47:1 47:0 29:0  # Ctrl+V
```

Key codes:
- 29: Ctrl
- 42: Shift
- 47: V

### Add Additional Actions

You can add additional key presses or actions after pasting:

```bash
# Paste text
echo "$final_text" | wl-copy
ydotool key 29:1 42:1 47:1 47:0 42:0 29:0

# Press Enter after pasting
sleep 0.1
ydotool key 28:1 28:0  # Enter
```

## Advanced: Systemd Service Options

### Auto-Restart Behavior

Edit service files in `~/.config/systemd/user/` to change restart behavior:

```ini
[Service]
Restart=always
RestartSec=5
StartLimitIntervalSec=300
StartLimitBurst=5
```

- `RestartSec`: Wait time before restart (seconds)
- `StartLimitBurst`: Max restart attempts
- `StartLimitIntervalSec`: Time window for restart limit

### Environment Variables

Add custom environment variables to service files:

```ini
[Service]
Environment="CUDA_VISIBLE_DEVICES=0"
Environment="CUSTOM_VAR=value"
```

After editing services:

```bash
systemctl --user daemon-reload
systemctl --user restart whisper-daemon whisper-hotkey
```

## Audio Input Configuration

### Select Specific Microphone

Edit `~/.local/bin/whisper-dictate` to specify your microphone:

```bash
# Find your microphone
pw-record --list-targets

# Use specific target (add to pw-record command)
pw-record --target=<your-microphone-id> output.wav
```

### Change Sample Rate

Default is 16kHz (optimal for Parakeet). To change:

```bash
pw-record --rate=48000 output.wav
```

**Note**: Higher sample rates increase file size without improving accuracy.

## Statistics Configuration

### Change Stats Database Location

Edit `~/.local/bin/whisper-daemon`:

```python
STATS_DB = os.path.expanduser("~/.local/share/whisper-dictation/stats.db")
```

### Disable Statistics

Comment out all `update_stats()` calls in the daemon.

### Reset Statistics

```bash
rm ~/.local/share/whisper-dictation/stats.db
# Stats will be recreated on next use
```

## Performance Tuning

### Reduce VRAM Usage

Edit `~/.local/bin/whisper-daemon` to use smaller precision:

```python
# Change from float32 to float16
model.half()  # Add this after model loading
```

### Increase Transcription Speed

Ensure GPU is not throttled:

```bash
nvidia-smi -q -d CLOCK
# Should show maximum clock speeds
```

### Multiple GPUs

To use a specific GPU:

Edit service file `~/.config/systemd/user/whisper-daemon.service`:

```ini
Environment="CUDA_VISIBLE_DEVICES=1"  # Use GPU 1
```

## Backup Configuration

Your configuration is stored in these locations:

- Scripts: `~/.local/bin/whisper-*`
- Services: `~/.config/systemd/user/whisper-*.service`
- Stats DB: `~/.local/share/whisper-dictation/stats.db`
- Auto-gain: `~/.config/whisper-dictation/autogain.json`

To backup:

```bash
tar -czf whisper-backup.tar.gz \
    ~/.local/bin/whisper-* \
    ~/.local/bin/whisperstats \
    ~/.config/systemd/user/whisper-*.service \
    ~/.config/systemd/user/ydotoold.service \
    ~/.local/share/whisper-dictation/stats.db \
    ~/.config/whisper-dictation/
```

## Next Steps

- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if something isn't working
- Check [DEVELOPMENT.md](DEVELOPMENT.md) to contribute improvements
- Read the main [README.md](../README.md) for usage tips
