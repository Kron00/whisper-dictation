# Voice Dictation Tools Comparison

Side-by-side comparison of features across major voice dictation tools.

---

## Tool Overview

| Tool | Platform | Processing | Price | Best For |
|------|----------|------------|-------|----------|
| **Wispr Flow** | Mac, Windows, iOS | Cloud | $12/mo | General productivity, cross-app dictation |
| **Superwhisper** | macOS, iOS | Local | Free tier, paid for more | Privacy-focused Mac users |
| **Dragon Professional** | Windows | Local | $699 one-time | Enterprise, legal, medical |
| **Talon** | Mac, Windows, Linux | Local | Free (donations) | Developers, RSI/accessibility |
| **macOS Dictation** | macOS | Local/Cloud | Free | Casual Mac users |
| **Windows Voice Access** | Windows 11 | Cloud | Free | Windows accessibility |
| **Nerd Dictation** | Linux | Local | Free/OSS | Linux enthusiasts |
| **Serenade** | Cross-platform | Local/Cloud | Free tier | Voice coding |
| **VS Code Speech** | VS Code | Local | Free | Coding in VS Code |

---

## Feature Matrix

### Core Dictation Features

| Feature | Wispr | Super-whisper | Dragon | Talon | macOS | Windows | Nerd Dict |
|---------|-------|---------------|--------|-------|-------|---------|-----------|
| Continuous dictation | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Streaming preview | Yes | Yes | Yes | Yes | Yes | Yes | No |
| Auto punctuation | Yes | Yes | Yes | Yes | Yes | Yes | No |
| Filler word removal | Yes | Yes | Yes | No | No | Yes* | No |
| GPU acceleration | Cloud | Yes | No | No | Yes | No | Yes (VOSK) |

*Windows 11 Fluid Dictation feature on Copilot+ PCs

### Vocabulary & Learning

| Feature | Wispr | Super-whisper | Dragon | Talon | macOS | Windows | Nerd Dict |
|---------|-------|---------------|--------|-------|-------|---------|-----------|
| Custom vocabulary | Yes | Yes | Yes | Yes | Limited | Limited | No |
| Auto-learn words | Beta | No | Yes | No | Via Contacts | No | No |
| Pronunciation training | No | No | Yes | No | No | No | No |
| Domain dictionaries | No | No | Yes (Legal/Medical) | Community | No | No | No |

### Voice Commands

| Feature | Wispr | Super-whisper | Dragon | Talon | macOS | Windows | Nerd Dict |
|---------|-------|---------------|--------|-------|-------|---------|-----------|
| Undo/scratch | Yes | Yes | Yes | Yes | Yes | Yes | No |
| Text selection | Limited | Limited | Yes | Yes | Yes | Yes | No |
| Delete commands | Yes | Yes | Yes | Yes | Yes | Yes | No |
| Navigation | Limited | Limited | Yes | Yes | Yes | Yes | No |
| Custom commands | No | Yes (modes) | Yes | Yes | Yes | Limited | No |

### Formatting & Context

| Feature | Wispr | Super-whisper | Dragon | Talon | macOS | Windows | Nerd Dict |
|---------|-------|---------------|--------|-------|-------|---------|-----------|
| Context-aware formatting | Yes | Yes | No | Yes | No | No | No |
| App-specific behavior | Yes | Yes | Yes | Yes | No | No | No |
| Markdown support | Yes | Yes | No | Yes | No | No | No |
| Code formatting | Yes | Yes | No | Yes | No | No | No |
| Snippets/templates | Yes | Limited | Yes | Yes | No | No | No |

### Language Support

| Feature | Wispr | Super-whisper | Dragon | Talon | macOS | Windows | Nerd Dict |
|---------|-------|---------------|--------|-------|-------|---------|-----------|
| Languages supported | 100+ | 100+ | 6 | Many | 60+ | 10+ | Many (VOSK) |
| Auto language detect | Yes | Yes | No | No | Yes | No | No |
| Multi-language per session | Yes | Yes | No | No | Yes | No | No |

### Mouse & System Control

| Feature | Wispr | Super-whisper | Dragon | Talon | macOS | Windows | Nerd Dict |
|---------|-------|---------------|--------|-------|-------|---------|-----------|
| Mouse control | No | No | Yes (grid) | Yes | Yes (grid) | Yes (grid) | No |
| Scrolling commands | No | No | Yes | Yes | Yes | Yes | No |
| App launching | No | No | Yes | Yes | Yes | Yes | No |
| Window management | No | No | Yes | Yes | Yes | Yes | No |
| Eye tracking | No | No | No | Yes | No | No | No |

### Coding Features

| Feature | Wispr | Super-whisper | Dragon | Talon | macOS | Windows | Nerd Dict |
|---------|-------|---------------|--------|-------|-------|---------|-----------|
| IDE integration | Yes (Cursor, VS Code) | No | Limited | Yes | No | No | No |
| Symbol dictation | Yes | No | No | Yes | No | No | No |
| Language-aware | Yes | No | No | Yes | No | No | No |
| Code navigation | Cursor ext | No | No | Yes (Cursorless) | No | No | No |

### Privacy & Processing

| Feature | Wispr | Super-whisper | Dragon | Talon | macOS | Windows | Nerd Dict |
|---------|-------|---------------|--------|-------|-------|---------|-----------|
| Offline capable | No | Yes | Yes | Yes | Yes* | No | Yes |
| On-device processing | No | Yes | Yes | Yes | Yes* | No | Yes |
| Data sent to cloud | Yes | Optional | No | No | Optional | Yes | No |
| HIPAA compliant | Yes | N/A | Yes | N/A | N/A | N/A | N/A |

*Requires Apple Silicon and supported language

### UI & Activation

| Feature | Wispr | Super-whisper | Dragon | Talon | macOS | Windows | Nerd Dict |
|---------|-------|---------------|--------|-------|-------|---------|-----------|
| Hotkey activation | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Wake word | No | No | No | No | No | No | No |
| System tray | Yes | Yes | Yes | Yes | Menu bar | Floating bar | No |
| Floating preview | Yes | Yes | Yes | Yes | Inline | Yes | No |
| Dictation history | No | Yes | No | No | No | No | No |

---

## Unique Features by Tool

### Wispr Flow
- **Tone Match:** Automatically adjusts formality based on destination app
- **IDE Extensions:** Deep Cursor and Windsurf integration for voice coding
- **Warp Terminal Integration:** Voice commands directly in terminal
- **Cross-device sync:** Settings sync across Mac, Windows, iOS

### Superwhisper
- **Multiple AI Models:** Choose between Nano, Fast, Pro, Ultra for speed vs accuracy
- **Context modes:** Selected text + clipboard + app context all available to AI
- **Custom modes:** Define your own processing with AI instructions
- **Fully offline:** All processing on device

### Dragon Professional
- **Voice profiles:** Train the system on your voice for higher accuracy
- **Auto Transcribe Folder Agent:** Batch process audio files
- **Enterprise management:** Centralized vocabulary and settings deployment
- **25+ years of development:** Most mature desktop dictation solution

### Talon
- **Cursorless integration:** Revolutionary visual code editing
- **Eye tracking:** Use gaze for cursor positioning
- **Pop/Hiss sounds:** Non-speech sounds as commands
- **Python scripting:** Unlimited customization
- **Community-driven:** Large library of community commands

### macOS Voice Control
- **Full system control:** Complete macOS accessibility solution
- **Number overlays:** Click any element by number
- **Drag and drop by voice:** Full mouse emulation
- **Native integration:** Works with all macOS apps

### Windows 11 Voice Access
- **Fluid Dictation:** AI-powered grammar and punctuation on Copilot+ PCs
- **Grid navigation:** 9-square grid for precise cursor placement
- **Voice commands for everything:** Full Windows control
- **Dictation + Command modes:** Switch between input modes

### Nerd Dictation
- **Single Python file:** Minimal, hackable codebase
- **Wayland support:** Works via dotool/ydotool
- **No background process:** Zero overhead when not in use
- **VOSK backend:** Good offline recognition

### Serenade
- **Open source:** Self-hostable
- **Language-aware:** Understands programming language context
- **Speech engine options:** Cloud or local processing
- **Cross-IDE:** Works with multiple editors

---

## Linux-Specific Considerations

### Tools with Native Linux Support
1. **Talon** - Full support, but X11 only (no Wayland)
2. **Nerd Dictation** - Native Linux, supports X11 and Wayland
3. **Serenade** - Cross-platform including Linux

### Tools Requiring Adaptation
1. **Superwhisper** - macOS only, but approach can be replicated
2. **Wispr Flow** - No Linux version, cloud-dependent features
3. **VS Code Speech** - Works on Linux through VS Code

### Linux-Specific Challenges
- Wayland compositors lack accessibility APIs that Talon needs
- No standardized dictation API across Linux desktops
- PulseAudio/PipeWire audio routing complexity
- Global hotkey registration varies by desktop environment
- X11 tools (xdotool) don't work on Wayland, need ydotool/dotool

### Recommended Linux Stack
- **Speech recognition:** faster-whisper (already in use)
- **Input simulation:** ydotool (Wayland) or xdotool (X11)
- **Audio capture:** PulseAudio/PipeWire
- **Hotkeys:** keyd, sway bindings, or similar
- **Notifications:** libnotify / notify-send
- **Tray icon:** GTK StatusIcon or AppIndicator
