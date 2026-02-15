# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Local GPU-accelerated voice dictation for Linux (Wayland/Niri). Double middle-click to record, speak, double middle-click to transcribe and paste. NVIDIA Parakeet TDT model stays hot in VRAM via a daemon.

## Build & Deploy

```bash
# Deploy scripts after editing
cp scripts/<script-name> ~/.local/bin/

# Build and deploy Rust overlay
cd whisper-flow-rs && cargo build --release && cp target/release/whisper-flow ~/.local/bin/

# Restart services after daemon/hotkey changes
systemctl --user restart whisper-daemon whisper-hotkey

# View daemon logs
journalctl --user -u whisper-daemon -f

# Check service status
systemctl --user status whisper-daemon whisper-hotkey
```

No test suite exists. Validate changes by running `whisper-dictate` manually and checking daemon logs.

## Architecture

### Component Map

```
whisper-hotkey (Python evdev, systemd service)
    │ detects double middle-click
    ▼
whisper-dictate (Bash, main orchestrator)
    ├── whisper-autogain (Bash) — sets optimal mic volume
    ├── whisper-flow-rs (Rust GTK4 overlay) — animated waveform pill
    ├── pw-record → /tmp/whisper-dictate.wav
    ├── whisper-stream (Bash) — background partial transcription preview
    │
    │  on stop:
    ├── sends WAV to whisper-daemon via /tmp/whisper-daemon.sock
    ├── wl-copy + sleep 50ms + ydotool paste
    └── whisper-learn (Python) — monitors clipboard 30s for corrections

whisper-daemon (Python, systemd service)
    ├── keeps Parakeet TDT model in VRAM (~2-3GB)
    ├── listens on Unix socket /tmp/whisper-daemon.sock
    ├── applies: Silero VAD → transcribe → punctuation → filler removal → dictionary
    └── logs to SQLite stats.db

whisperstats (Python GTK4/libadwaita)
    ├── Stats tab: words dictated, time saved, WPM, recent dictations
    └── Dictionary tab: add/delete entries
```

### IPC via Temp Files

| File | Purpose |
|------|---------|
| `/tmp/whisper-daemon.sock` | Unix socket for daemon communication |
| `/tmp/whisper-dictate.state` | "recording" or "transcribing" (overlay reads this) |
| `/tmp/whisper-dictate.wav` | Live audio capture (overlay reads for waveform) |
| `/tmp/whisper-daemon.status` | "ready", "starting", "error: ...", "stopped" |
| `/tmp/whisper-flow.mode` | "regex" or "llm" rewrite mode |
| `/tmp/whisper-noise-reduction.enabled` | Presence = noise reduction on |

### Data Files

| File | Purpose |
|------|---------|
| `~/.config/whisper-dictation/dictionary.json` | Flat JSON array: `[{"spoken": "...", "replacement": "..."}]` |
| `~/.local/share/whisper-dictation/stats.db` | SQLite dictation history |

## Tech Stack

- **Python 3.12** — daemon, hotkey, stats, learn, correct
- **Bash** — dictate, stream, flow control, autogain, mode, noise
- **Rust 2024 edition** — overlay binary (gtk4 0.10, libadwaita 0.8, gtk4-layer-shell 0.7)
- **Parakeet TDT** via NeMo toolkit (not faster-whisper despite script names)
- **PipeWire** for audio capture (`pw-record`)
- **evdev** for mouse input grabbing
- **wl-copy/ydotool** for clipboard and paste

## Rust Overlay (whisper-flow-rs)

Single-file binary (`src/main.rs`, ~305 lines). Uses Cell/RefCell for shared state, glib timeout callbacks for animation (16ms), audio reads (50ms), and state file polling (150ms). Links libgtk4-layer-shell directly — no LD_PRELOAD needed. Aggressive release profile: LTO, single codegen unit, strip, panic=abort → 340K binary.

**Key:** Uses gtk4 re-exported cairo/gio/glib. Do NOT add separate cairo/gio/glib crate dependencies — causes version conflicts.

## Environment Gotchas

- **Niri compositor** with DMS shell (not GNOME) — `WAYLAND_DISPLAY=wayland-1`
- **whisper-hotkey service** doesn't inherit `WAYLAND_DISPLAY` from systemd — must detect dynamically from `/run/user/1000/wayland-*`
- **wl-copy race condition** — 50ms sleep required between `wl-copy` and `ydotool` paste
- **.desktop files** must have Unix line endings or DMS spotlight ignores them
- **Dictionary format** — daemon accepts both flat array and `{"entries": [...]}` wrapper

## Dictionary Processing Pipeline

1. **Pre-processing:** Dictionary words fed as `initial_prompt` (Glossary) + `hotwords` to bias the model
2. **Transcription:** Parakeet TDT with Silero VAD
3. **Post-processing:** Punctuation commands → filler removal → dictionary regex replacement (whole-word, case-insensitive)
4. **Auto-learn:** `whisper-learn` watches clipboard 30s after dictation, detects corrections, saves to dictionary
