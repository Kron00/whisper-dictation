# Whisper Dictation - Feature Ideas

Pick the features you want to add. Organized by complexity and impact.

---

## Already Implemented
- [x] Double middle-click trigger
- [x] GPU-accelerated transcription (faster-whisper)
- [x] Daemon architecture (model in VRAM)
- [x] Streaming preview (partial transcription)
- [x] Filler word removal
- [x] Whisper mode (low-volume speech)
- [x] Auto-pause/resume music

---

## TIER 1: High Impact, Quick Wins

### [ ] Voice Editing Commands
"Undo that", "delete that", "scratch that" to remove last dictation without keyboard.
- Track last N dictation segments
- Detect command phrases before transcription
- Critical for maintaining flow

### [ ] System Tray Status Indicator
Visual icon showing ready/recording/processing state.
- Different icons per state
- Right-click menu for mode switching
- Tooltip with current mode

### [ ] Dictation History
SQLite log of all dictations with timestamps.
- Searchable history
- One-click copy of previous dictations
- Statistics over time

### [ ] Custom Vocabulary
Add names, technical terms, jargon that Whisper misrecognizes.
- Simple text file of custom words
- Passed to Whisper via prompt parameter
- Example: "kubectl", "numpy", your name

### [ ] Snippets/Templates
Voice triggers for common text.
- "Insert signature" -> full email signature
- "My address" -> formatted address
- Variables: {{date}}, {{clipboard}}

---

## TIER 2: Nice Enhancements

### [ ] Context-Aware Formatting
Different processing per application.
- Terminals: no auto-capitalization
- Slack/Discord: casual, shorter
- Email: formal tone
- Based on active window detection

### [ ] LLM Post-Processing (Optional)
Local LLM (Ollama) to clean up transcription.
- Fix grammar and punctuation
- Better capitalization
- Adds ~500-1500ms latency
- Uses Llama 3 8B or similar (fits in VRAM with Whisper)

### [ ] Multiple Hotkey Configurations
Configurable shortcuts for different functions.
- Different keys for start/stop
- Mode toggle shortcut
- Cancel recording hotkey

### [ ] Clipboard Options
Choose output behavior.
- Paste directly (current)
- Clipboard only (no paste)
- Both (paste AND keep in clipboard)

### [X] Basic Statistics
Track usage metrics.
- Words dictated per day
- Time saved vs typing estimate
- Display in tray menu

---

## TIER 3: Power User Features

### [X] Multi-Language Auto-Detection
Auto-detect language without manual selection.
- Whisper supports 99 languages
- Detect from first few seconds of audio
- Per-app language preferences

### [ ] Text Navigation Commands
"Select last sentence", "go to end", "delete last 3 words"
- More complex command parsing
- Selection via keyboard shortcuts
- Application-specific behavior

### [ ] Noise Reduction
Pre-process audio to remove background noise.
- Use RNNoise or PipeWire noise suppression
- Filter keyboard clicks
- Better accuracy in noisy environments

### [ ] Audio Recording/Playback
Save audio alongside transcription.
- Review uncertain transcriptions
- Playback synced to text
- Meeting records

### [ ] Wake Word Activation
"Hey Computer" to start listening (hands-free).
- Uses Picovoice Porcupine (low CPU)
- Custom wake phrases available
- Completely hands-free activation

---

## TIER 4: Advanced/Specialized

### [ ] Voice-Controlled Mouse
Control cursor by voice.
- Grid overlay with numbered zones
- "Mouse up 50", "click", "double click"
- Full hands-free operation

### [ ] IDE Integration
Deep VS Code integration.
- "Go to line 42", "run tests"
- Symbol dictation ("equals", "arrow")
- Possible Copilot integration

### [ ] Privacy Mode / App Blocklist
Auto-disable for sensitive apps.
- Block recording in password managers
- Configurable app patterns
- Prevent accidental capture

### [ ] Pop/Hiss Sound Commands
Non-speech sounds as shortcuts.
- Pop sound -> click
- Hiss -> scroll
- Requires audio classifier training

### [ ] Homophones Selection
Quick picker for ambiguous words (their/there/they're).
- Popup when homophones detected
- Number shortcuts to select
- Context-aware suggestions

---

## Quick Wins (Easy to Add)

### [ ] Cancel Command
Hotkey to cancel current recording without transcribing.

### [ ] Configurable Silence Timeout
Adjust how long silence triggers end of dictation.

### [ ] Disable Start Sound Option
Some users prefer silent operation.

### [ ] Simple Text Log
Plain text file of all dictations (before SQLite history).

---

## My Recommendations

**Start with these 5:**
1. Voice editing commands ("undo that") - biggest quality of life improvement
2. System tray indicator - always know what state you're in
3. Snippets - huge time saver if you have repetitive text
4. Custom vocabulary - fixes persistent misrecognitions
5. Cancel hotkey - escape hatch when you start recording by accident

**Then consider:**
- Dictation history (if you want to review/search past dictations)
- LLM post-processing (if you need polished output for emails/docs)
- Context-aware formatting (if you use many different apps)

---

## Notes

- All features run locally, no cloud services
- RTX 3090 can run Whisper + 8B LLM simultaneously
- Full research in `research/voice-dictation-features/`
