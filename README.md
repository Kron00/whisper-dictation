# Voice Dictation for Linux

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Platform](https://img.shields.io/badge/platform-Linux%20ONLY-red.svg)

> **⚠️ Linux Only** - This software is designed exclusively for Linux systems with Wayland/GNOME. It will not work on Windows or macOS.

A local voice-to-text dictation system for Linux using NVIDIA Parakeet TDT with GPU acceleration. Features instant transcription, spoken punctuation commands, filler word removal, auto-pause music, and statistics tracking.

## Quick Start

```bash
git clone https://github.com/Kron00/whisper-dictation.git
cd whisper-dictation
./install.sh
```

Double middle-click to start recording, speak, then double middle-click again to paste.

For detailed installation instructions, see [docs/INSTALLATION.md](docs/INSTALLATION.md).

## Features

- **NVIDIA Parakeet TDT 0.6B v2** - 50x faster than Whisper, better accuracy (6.05% WER)
- **Instant transcription** - Model stays hot in VRAM via daemon
- **Double middle-click trigger** - Prevents accidental activations
- **Spoken punctuation** - Say "period", "comma", "question mark", etc.
- **Filler word removal** - Automatically removes "um", "uh", "like", etc.
- **Auto-pause music** - Pauses playing media during recording, resumes after
- **Statistics tracking** - WhisperStats app shows words dictated, time saved, WPM
- **GPU-accelerated** - RTX 3090, ~2-3GB VRAM usage
- **No cloud services** - Runs entirely locally

## Requirements

- NVIDIA GPU with CUDA support
- PipeWire audio
- Wayland (GNOME)
- Python 3.12

## Installation

### Automated Installation (Recommended)

```bash
git clone https://github.com/Kron00/whisper-dictation.git
cd whisper-dictation
./install.sh
```

The installer will:
- Check prerequisites (GPU, Python 3.12, CUDA)
- Install system dependencies
- Create Python virtual environment
- Install scripts and systemd services
- Start and validate the installation

### Manual Installation

For manual installation or detailed instructions, see [docs/INSTALLATION.md](docs/INSTALLATION.md).

## Usage

1. **Double middle-click** to start recording (you'll hear a sound)
2. **Speak** your text with punctuation commands
3. **Double middle-click** again to stop and transcribe
4. Text is automatically pasted (Ctrl+Shift+V for plain text)

### Spoken Punctuation Commands

| Say This | Get This |
|----------|----------|
| period | . |
| comma | , |
| question mark | ? |
| exclamation point | ! |
| colon | : |
| semicolon | ; |
| new line | (line break) |
| new paragraph | (double line break) |
| open quote / close quote | " |
| open paren / close paren | ( ) |
| hyphen / dash | - |
| ellipsis | ... |

### Statistics App

```bash
whisperstats   # Launch the statistics dashboard
```

Shows:
- Words dictated today / all time
- Time saved vs typing
- Your speaking rate (WPM)
- Recent dictations
- Languages detected

## Configuration

Whisper Dictation can be customized extensively. For complete configuration options, see [docs/CONFIGURATION.md](docs/CONFIGURATION.md).

**Quick configurations:**

- **Sound effects** - Change start/stop beep sounds
- **Double-click threshold** - Adjust sensitivity (default: 300ms)
- **Filler words** - Customize words to remove ("um", "uh", etc.)
- **Punctuation commands** - Add/modify spoken punctuation
- **Noise reduction** - Enable background noise filtering
- **Auto-gain** - Automatic microphone volume adjustment
- **Flow mode** - LLM post-processing for grammar correction

## Files

| File | Purpose |
|------|---------|
| `~/.local/bin/whisper-daemon` | Python daemon - Parakeet model in VRAM |
| `~/.local/bin/whisper-dictate` | Main bash script - recording/transcription |
| `~/.local/bin/whisper-hotkey` | Python evdev listener - double-click detection |
| `~/.local/bin/whisperstats` | GTK4 statistics dashboard |
| `~/.local/bin/whisper-mode` | Mode toggle script |

### Systemd Services

| Service | Purpose |
|---------|---------|
| `whisper-daemon.service` | Loads Parakeet model into VRAM on login |
| `whisper-hotkey.service` | Listens for middle-click |
| `ydotoold.service` | Keyboard simulation daemon |

### Data Files

| File | Purpose |
|------|---------|
| `~/.local/share/whisper-dictation/stats.db` | SQLite database with dictation history |
| `~/.cache/huggingface/` | Downloaded Parakeet model cache |

## Troubleshooting

For detailed troubleshooting, see [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

**Quick diagnostics:**

```bash
# Check service status
systemctl --user status whisper-daemon whisper-hotkey

# View daemon logs
journalctl --user -u whisper-daemon -f

# Check GPU
nvidia-smi

# Check daemon status
cat /tmp/whisper-daemon.status
```

## Hardware

- GPU: NVIDIA RTX 3090 (24GB VRAM)
- Microphone: HyperX QuadCast
- Mouse: Logitech USB Receiver

## Documentation

- [Installation Guide](docs/INSTALLATION.md) - Detailed installation instructions
- [Configuration Guide](docs/CONFIGURATION.md) - Customize settings
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md) - Common issues and solutions
- [Development Guide](docs/DEVELOPMENT.md) - Contributing and architecture

## Research

The `research/` folder contains comprehensive documentation of design decisions:

- `research/whisper-stt-models-2025/` - Model comparison and benchmarks
- `research/spoken-punctuation/` - Punctuation command implementation
- `research/voice-dictation-features/` - Feature analysis and roadmap

These documents provide context for why certain technical choices were made.

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

For development setup and guidelines, see [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md).

### Areas for Contribution

- Automated testing
- CPU fallback mode (non-NVIDIA GPUs)
- Additional mouse/keyboard combinations
- Packaging (RPM, DEB, AUR)
- Documentation improvements
- Bug fixes and performance optimizations

## Uninstall

To remove Whisper Dictation:

```bash
cd whisper-dictation
./uninstall.sh
```

The uninstaller will prompt you about removing statistics, configuration, and model cache.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- **NVIDIA Parakeet TDT** - Fast and accurate speech recognition model
- **NVIDIA NeMo Toolkit** - Framework for conversational AI
- **ydotool** - Wayland keyboard/mouse automation
- **PipeWire** - Modern Linux audio system
- All contributors and users of this project

## Support

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/Kron00/whisper-dictation/issues)
- **Documentation**: Check the docs/ folder for detailed guides
- **Community**: Share your experiences and help others

---

Made with 🎙️ for Linux voice dictation enthusiasts
