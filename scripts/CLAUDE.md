# Whisper Dictation - Project Context

## Architecture

- **whisper-daemon** - Python systemd service, keeps faster-whisper model in VRAM, listens on Unix socket `/tmp/whisper-daemon.sock`
- **whisper-dictate** - Bash script, toggles recording/transcription via `pw-record` + daemon socket, pastes via `wl-copy` + `ydotool`
- **whisper-flow** - Rust GTK4 overlay binary (`whisper-flow-rs/`), shows animated waveform pill at bottom of screen during dictation
- **whisper-hotkey** - Python evdev listener (systemd user service), grabs Logitech mouse, detects double middle-click → triggers whisper-dictate
- **whisper-stream** - Streaming preview (launched by whisper-dictate during recording)
- **whisperstats** - Python GTK4/libadwaita app with Stats + Dictionary tabs
- **whisper-autogain** - Bash script for microphone volume optimization

## Key Paths

| What | Path |
|------|------|
| Daemon service | `~/.config/systemd/user/whisper-daemon.service` |
| Hotkey service | `~/.config/systemd/user/whisper-hotkey.service` |
| Dictionary JSON | `~/.config/whisper-dictation/dictionary.json` |
| Stats DB | `~/.local/share/whisper-dictation/stats.db` |
| State file | `/tmp/whisper-dictate.state` (recording/transcribing) |
| Audio file | `/tmp/whisper-dictate.wav` |
| Installed binaries | `~/.local/bin/whisper-*` |
| Rust overlay source | `whisper-flow-rs/` |

## Dictionary System

- **Format:** Flat JSON array: `[{"spoken": "ghosty", "replacement": "Ghostty"}, ...]`
- **Daemon loads** via `load_dictionary()` with mtime caching
- **Post-processing:** Regex whole-word case-insensitive replacement after transcription
- **Pre-processing (TODO):** Pass words to faster-whisper `initial_prompt` + `hotwords` params
- **GUI:** whisperstats Dictionary tab (add/delete entries)

## Environment Gotchas

- **WAYLAND_DISPLAY:** Niri uses `wayland-1`, NOT `wayland-0`. The whisper-hotkey service doesn't inherit this from systemd - must detect dynamically from `/run/user/1000/wayland-*` sockets
- **LD_PRELOAD:** NOT needed for the Rust overlay (links libgtk4-layer-shell directly). WAS needed for the Python version
- **wl-copy race:** Need 50ms sleep between `wl-copy` and `ydotool` paste so compositor registers new clipboard content
- **.desktop files:** Must have Unix line endings (`\n`), NOT Windows (`\r\n`) - DMS spotlight ignores files with carriage returns

## Deploy Checklist

After editing scripts, deploy to `~/.local/bin/`:
```bash
cp scripts/whisper-dictate ~/.local/bin/
cp scripts/whisperstats ~/.local/bin/
# Rust overlay: cd whisper-flow-rs && cargo build --release && cp target/release/whisper-flow ~/.local/bin/
# Restart services if daemon/hotkey changed:
# systemctl --user restart whisper-daemon whisper-hotkey
```

## Tech Stack

- **Compositor:** Niri (Wayland) with DMS shell
- **Rust:** 1.92.0 (overlay binary, 338K stripped)
- **Python:** 3.12 (daemon, hotkey, stats)
- **GTK4/libadwaita:** UI framework for overlay and stats app
- **faster-whisper:** CTranslate2-based Whisper (model kept in VRAM)
- **Input:** evdev grab + uinput passthrough (whisper-hotkey)
