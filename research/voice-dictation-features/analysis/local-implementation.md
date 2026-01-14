# Features Practical for Local Linux Implementation

Analysis of which features can be implemented locally without cloud dependencies, with technical considerations.

---

## FULLY LOCAL IMPLEMENTATIONS

These features can be implemented entirely on-device with no cloud services.

### 1. Voice Editing Commands

**Technical Approach:**
```
1. After Whisper transcription, check for command phrases
2. If command detected, execute action instead of typing text
3. Track history of recent dictations for undo capability
```

**Commands to Implement:**
- "undo that" / "scratch that" -> Delete last dictation
- "delete that" -> Delete selection or last phrase
- "delete last N words" -> Precise deletion
- "undo" -> Send Ctrl+Z
- "redo" -> Send Ctrl+Y

**Dependencies:** xdotool/ydotool, text history buffer

**Latency Impact:** Minimal (command detection is fast)

---

### 2. Custom Vocabulary

**Technical Approach:**
```
Option A: Whisper Prompt Parameter
- Load word list from config file
- Pass to Whisper via initial_prompt parameter
- Biases recognition toward listed words

Option B: Post-Processing Replacement
- After transcription, check for known misrecognitions
- Replace with correct spelling from dictionary
- e.g., "cube cuttle" -> "kubectl"
```

**File Format:**
```json
{
  "words": [
    {"spoken": "kubernetes", "written": "Kubernetes"},
    {"spoken": "cube cuddle", "written": "kubectl"},
    {"spoken": "pie torch", "written": "PyTorch"}
  ]
}
```

**Dependencies:** Config file parser, string matching

**Latency Impact:** Negligible

---

### 3. Snippet/Template System

**Technical Approach:**
```
1. Define snippets in config: trigger phrase -> expansion
2. Check transcription for trigger phrases
3. If found, replace with expansion text
4. Support variables: {{date}}, {{time}}, {{clipboard}}
```

**Config Example:**
```yaml
snippets:
  "my email": "user@example.com"
  "my address": "123 Main St\nCity, State 12345"
  "date today": "{{date:YYYY-MM-DD}}"
  "insert signature": |
    Best regards,
    Your Name
    {{clipboard}}
```

**Dependencies:** Template engine (simple string substitution)

**Latency Impact:** Negligible

---

### 4. Context-Aware Formatting

**Technical Approach:**
```
1. Get active window: xdotool getwindowfocus getwindowname
2. Match against rules in config
3. Apply appropriate formatting options
```

**Config Example:**
```yaml
contexts:
  - match: ".*code.*|.*Code.*|.*vim.*|.*terminal.*"
    options:
      auto_capitalize: false
      auto_punctuate: false
      code_mode: true

  - match: ".*Slack.*|.*Discord.*"
    options:
      casual_mode: true
      shorter_sentences: true

  - match: ".*Mail.*|.*Outlook.*|.*Gmail.*"
    options:
      formal_mode: true
      full_punctuation: true
```

**Dependencies:** Window name detection, rule matching

**Latency Impact:** Minimal (one syscall)

---

### 5. LLM Post-Processing (Local)

**Technical Approach:**
```
1. Send Whisper output to local LLM via Ollama API
2. Use context-specific prompt for cleanup
3. Return cleaned text

Prompt example:
"Clean up this dictation. Fix grammar, punctuation, and
capitalization. Remove filler words and false starts.
Keep the meaning intact. Context: email composition.
Text: {transcription}"
```

**Model Options:**
- Llama 3.2 3B - Fast, good for simple cleanup
- Llama 3.1 8B - Better quality, still fast on RTX 3090
- Mistral 7B - Good balance of speed and quality
- Qwen2.5 7B - Strong performance

**Dependencies:** Ollama or llama.cpp, model weights

**Latency Impact:** Moderate (500ms-2s depending on model and text length)

**Optimization:** Make optional, use small models, batch short texts

---

### 6. Dictation History

**Technical Approach:**
```
SQLite database with schema:
- id: INTEGER PRIMARY KEY
- timestamp: DATETIME
- text: TEXT
- audio_path: TEXT (optional)
- app_context: TEXT
- word_count: INTEGER
```

**Features:**
- CLI: `dict-history search "search term"`
- CLI: `dict-history list --today`
- CLI: `dict-history copy 42` (copy entry 42 to clipboard)

**Dependencies:** SQLite3

**Latency Impact:** Negligible (async write)

---

### 7. Multiple Microphone Profiles

**Technical Approach:**
```
1. Detect current audio device from PulseAudio/PipeWire
2. Load corresponding profile: gain, noise gate, sample rate
3. Apply settings before recording

Profiles:
- laptop_mic: gain=1.5, noise_gate=0.01
- usb_headset: gain=1.0, noise_gate=0.005
- blue_yeti: gain=0.8, noise_gate=0.008
```

**Dependencies:** PulseAudio/PipeWire API

**Latency Impact:** None (applied during setup)

---

### 8. Noise Reduction

**Technical Approach:**
```
Option A: PulseAudio Module
- pactl load-module module-echo-cancel
- Built-in, easy to enable

Option B: RNNoise
- Pipe audio through RNNoise before Whisper
- Better quality, more CPU usage

Option C: Pre-trained Denoiser
- Use denoiser library (Meta's demucs or similar)
- Best quality, more resources
```

**Dependencies:** PulseAudio or RNNoise

**Latency Impact:** Low (10-50ms)

---

### 9. Wake Word Detection

**Technical Approach:**
```
1. Use Picovoice Porcupine for always-on listening
2. Very low CPU usage (~1%)
3. When wake word detected, start main recording
4. Custom wake words require Porcupine Console (free tier available)
```

**Built-in Wake Words:** "Computer", "Jarvis", "Hey Google" (for testing)

**Custom Wake Words:** Use Porcupine Console to train

**Dependencies:** pvporcupine library (has Linux ARM/x86 support)

**Latency Impact:** ~100ms for wake word detection

---

### 10. System Tray Indicator

**Technical Approach:**
```
GTK3 StatusIcon or AppIndicator:
- Green icon: Ready
- Red icon: Recording
- Yellow icon: Processing
- Gray icon: Disabled

Right-click menu:
- Start/Stop
- Mode selection
- Settings
- Statistics
- Quit
```

**Dependencies:** GTK3 or Qt, or simple tray library like pystray

**Latency Impact:** None

---

### 11. Multi-Language Support

**Technical Approach:**
```
Option A: User Selection
- Config option: language = "en" or "es" or "de"
- Pass to Whisper

Option B: Auto-Detection
- Use Whisper's detect_language() on first 30 seconds
- Or shorter segment for faster detection
- Set detected language for full transcription

Option C: Mixed Languages
- Whisper handles code-switching reasonably well
- May need larger model for best results
```

**Dependencies:** Whisper model (already available)

**Latency Impact:** Auto-detection adds ~200-500ms

---

### 12. Voice Mouse Control

**Technical Approach:**
```
Grid System:
1. Display numbered overlay on screen (3x3 or 9x9)
2. User says number to narrow down or click
3. "Click 5" -> click center, "Zoom 5, click 3" -> precise

Directional:
1. "Mouse left 100" -> move left 100 pixels
2. "Click" -> left click
3. "Double click", "Right click" -> variants
```

**Dependencies:** Screen overlay (GTK/Cairo), xdotool/ydotool

**Latency Impact:** Grid rendering ~50ms

---

## FEATURES REQUIRING SIGNIFICANT EFFORT

### Cursorless-Style Code Editing
- Requires VS Code extension development
- Complex visual overlay system
- Consider integrating with existing Talon/Cursorless instead

### Full IDE Integration
- Each IDE needs custom extension
- VS Code has existing speech extension as reference
- Could simulate most features via keyboard shortcuts

### Eye Tracking
- Requires specific hardware (Tobii)
- Talon has this built-in if needed

---

## FEATURES NOT PRACTICAL LOCALLY

### Wispr Flow's Tone Matching
- Requires large LLM and sophisticated prompting
- Could approximate with local LLM but won't match cloud quality

### Enterprise Compliance Features (SOC 2, HIPAA)
- Organizational requirements, not technical features
- Local processing inherently more private

### Cross-Device Sync
- Would require setting up your own sync infrastructure
- Consider simple file-based sync (Syncthing)

---

## RECOMMENDED TECH STACK

```
Core:
- Python 3.10+ for main application
- faster-whisper for transcription (already in use)
- SQLite for dictation history
- TOML/YAML for configuration

Audio:
- PipeWire/PulseAudio for audio capture
- RNNoise for noise reduction (optional)
- Picovoice Porcupine for wake words (optional)

Input Simulation:
- ydotool for Wayland
- xdotool for X11
- python-xlib as fallback

UI:
- pystray or GTK3 for system tray
- GTK/Cairo for overlays (mouse grid)
- libnotify for notifications

AI (Optional):
- Ollama for local LLM post-processing
- Smaller models (3B-8B) for speed
```

---

## PERFORMANCE CONSIDERATIONS

With RTX 3090 and daemon architecture:

| Feature | Added Latency | GPU Memory | CPU Usage |
|---------|---------------|------------|-----------|
| Whisper large-v3 | baseline | ~2GB | Low |
| LLM post-process (8B) | +500-1500ms | +5-8GB | Low |
| LLM post-process (3B) | +200-500ms | +3GB | Low |
| Wake word (Porcupine) | continuous | 0 | ~1% |
| Noise reduction | +20-50ms | 0 | Low |
| Context detection | +5ms | 0 | Negligible |

**Recommendation:** Keep LLM post-processing optional. With 24GB VRAM on RTX 3090, can easily run Whisper + 8B LLM simultaneously if desired.
