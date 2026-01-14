# Implementation Priority Guide

Features prioritized by impact, implementation complexity, and practicality for a local Linux system.

---

## TIER 1: HIGH IMPACT, MODERATE COMPLEXITY
*Recommend implementing first - significant UX improvements*

### 1. Voice Editing Commands
**Features:** "Undo that", "delete that", "scratch that", "delete last [n] words"
**Complexity:** Medium
**Dependencies:** Command detection, text tracking
**Implementation Notes:**
- Detect command phrases before/after transcription
- Track last N dictation segments for undo capability
- Use xdotool/ydotool for selection and deletion
**Impact:** Critical for maintaining dictation flow without keyboard

### 2. Custom Vocabulary / Personal Dictionary
**Features:** Custom word list, pronunciation hints, technical terms
**Complexity:** Medium
**Dependencies:** Whisper prompt parameter, optional LLM post-processing
**Implementation Notes:**
- Pass word list to Whisper via prompt parameter
- Store in simple text/JSON file for easy editing
- Consider frequency-based sorting
- Add UI for managing words
**Impact:** Dramatically improves accuracy for names, technical terms

### 3. Snippet/Template System
**Features:** Voice-triggered text expansion, custom shortcuts
**Complexity:** Medium
**Dependencies:** Trigger phrase detection
**Implementation Notes:**
- Define snippets in config file (trigger -> expansion)
- Detect triggers before sending to Whisper or post-process
- Support variables like {{date}}, {{clipboard}}
**Impact:** Massive time savings for repetitive text

### 4. Dictation History
**Features:** Searchable log of all dictations with timestamps
**Complexity:** Low-Medium
**Dependencies:** SQLite or similar storage
**Implementation Notes:**
- Log each dictation with timestamp, app context, text
- Simple CLI or GUI for searching history
- Option to copy previous dictation to clipboard
**Impact:** Never lose dictated content, valuable for review

### 5. System Tray Status Indicator
**Features:** Visual state indicator, quick mode switching
**Complexity:** Low-Medium
**Dependencies:** GTK/Qt tray library
**Implementation Notes:**
- Show different icons for: ready, recording, processing
- Right-click menu for mode switching, settings access
- Tooltip showing current mode and stats
**Impact:** Better UX, always know system state

---

## TIER 2: GOOD ENHANCEMENTS, REASONABLE EFFORT
*Implement after Tier 1 for a polished experience*

### 6. Context-Aware Formatting
**Features:** Different processing per application
**Complexity:** Medium
**Dependencies:** Window detection, configurable rules
**Implementation Notes:**
- Use `xdotool getwindowfocus getwindowname` or similar
- Define rules in config: app pattern -> formatting options
- Examples: disable auto-capitalize in terminals, enable markdown in notes
**Impact:** Smarter output without manual mode switching

### 7. LLM Post-Processing (Optional)
**Features:** Grammar correction, improved punctuation, cleanup
**Complexity:** Medium-High
**Dependencies:** Local LLM (Ollama), latency considerations
**Implementation Notes:**
- Make optional/configurable (adds latency)
- Use small, fast models (Llama 3 8B, Mistral 7B)
- Pre-define prompts per context/application
- Cache model in memory for faster response
**Impact:** Higher quality output, especially for formal writing

### 8. Multiple Hotkey Configurations
**Features:** Different shortcuts for different modes/functions
**Complexity:** Low
**Dependencies:** Hotkey library (pynput or similar)
**Implementation Notes:**
- Configurable hotkeys for: start/stop, cancel, mode toggle
- Support modifier combinations
- Per-mode shortcuts if multiple modes exist
**Impact:** Flexibility for power users

### 9. Clipboard Output Options
**Features:** Paste, clipboard-only, or both
**Complexity:** Low
**Dependencies:** Clipboard handling
**Implementation Notes:**
- Config option: "paste", "clipboard", "both"
- "Both" copies to clipboard AND pastes
- Integrates well with clipboard managers
**Impact:** Flexibility for different workflows

### 10. Basic Statistics
**Features:** Words dictated, time saved, daily/weekly counts
**Complexity:** Low
**Dependencies:** Dictation logging
**Implementation Notes:**
- Increment counters on each dictation
- Store in simple file or SQLite
- Display in tray menu or separate command
**Impact:** Motivation, insight into usage patterns

---

## TIER 3: POWER USER FEATURES
*Nice to have for advanced users*

### 11. Multi-Language Auto-Detection
**Features:** Automatic language switching without manual selection
**Complexity:** Medium
**Dependencies:** Whisper language detection
**Implementation Notes:**
- Use Whisper's detect_language() on initial audio
- Or configure preferred language list (up to 4-5)
- Consider per-application language preferences
**Impact:** Essential for multilingual users

### 12. Text Selection/Navigation Commands
**Features:** "Select last sentence", "go to line N", navigation by voice
**Complexity:** Medium-High
**Dependencies:** Command parsing, text context tracking
**Implementation Notes:**
- More complex command grammar needed
- May need clipboard manipulation to select text
- Application-specific behavior
**Impact:** More complete hands-free editing

### 13. Noise Reduction
**Features:** Background noise filtering, echo cancellation
**Complexity:** Medium
**Dependencies:** RNNoise or similar
**Implementation Notes:**
- Can use PulseAudio noise suppression module
- Or pipe through RNNoise before Whisper
- Consider training custom noise gate for keyboard sounds
**Impact:** Better accuracy in noisy environments

### 14. Audio Recording for Playback
**Features:** Save audio with transcription for review
**Complexity:** Low-Medium
**Dependencies:** Audio file storage
**Implementation Notes:**
- Option to save raw audio alongside text
- Store with matching timestamps
- Simple playback interface
**Impact:** Useful for verifying uncertain transcriptions

### 15. Wake Word Activation
**Features:** "Hey Computer" or custom phrase to start listening
**Complexity:** Medium-High
**Dependencies:** Picovoice Porcupine or similar
**Implementation Notes:**
- Porcupine has good Linux support, low resource usage
- Runs continuously in background (low CPU)
- Triggers main recognition when wake word detected
- Custom wake words require Picovoice console
**Impact:** Fully hands-free activation

---

## TIER 4: ADVANCED/SPECIALIZED
*For specific use cases or future development*

### 16. Voice-Controlled Mouse
**Features:** Grid overlay, cursor movement, clicking by voice
**Complexity:** High
**Dependencies:** Screen overlay, command parsing
**Implementation Notes:**
- Numbered grid overlay system (like macOS Voice Control)
- "Click 4-7" to click zone, or "zoom 4" then "click 3"
- Or directional: "mouse up 50 pixels"
**Impact:** Full accessibility without physical mouse

### 17. IDE Integration
**Features:** Deep integration with VS Code or other editors
**Complexity:** High
**Dependencies:** Editor extension development
**Implementation Notes:**
- VS Code has built-in speech extension as reference
- Would need extension for proper integration
- Can simulate most features with keyboard shortcuts
**Impact:** Voice-first programming workflow

### 18. Cursorless-Style Code Editing
**Features:** Visual hats on code elements for voice reference
**Complexity:** Very High
**Dependencies:** Talon + Cursorless
**Implementation Notes:**
- Consider integrating with existing Talon ecosystem
- Cursorless is a VS Code extension
- Requires significant learning curve
**Impact:** Extremely efficient voice coding

### 19. Pop/Hiss Sound Commands
**Features:** Non-speech sounds as shortcuts
**Complexity:** High
**Dependencies:** Audio classifier training
**Implementation Notes:**
- Train small model to detect pop, hiss, click sounds
- Map to common actions (click, scroll)
- Talon has this built-in
**Impact:** Faster than speaking for common actions

### 20. Privacy Mode / App Blocklist
**Features:** Auto-disable for sensitive applications
**Complexity:** Low
**Dependencies:** Window detection
**Implementation Notes:**
- Config file with app patterns to block
- Check before starting recording
- Optional: show warning when blocked app detected
**Impact:** Prevent accidental recording of sensitive content

---

## QUICK WINS
*Low effort, immediate value*

1. **Configurable silence timeout** - Allow users to adjust how long silence triggers end of dictation
2. **Cancel command** - Hotkey or voice command to cancel current recording
3. **Sound feedback options** - Beep on start/stop (optional, some prefer silence)
4. **Log file with timestamps** - Simple text log of all dictations for manual review
5. **Man page / help command** - Document all voice commands and config options

---

## IMPLEMENTATION ORDER RECOMMENDATION

**Phase 1 (Core):**
1. Voice editing commands (undo, delete)
2. System tray indicator
3. Basic dictation history

**Phase 2 (Personalization):**
4. Custom vocabulary
5. Snippet system
6. Multiple hotkey configs

**Phase 3 (Intelligence):**
7. Context-aware formatting
8. LLM post-processing (optional)
9. Statistics

**Phase 4 (Advanced):**
10. Multi-language support
11. Voice navigation commands
12. Wake word activation

**Phase 5 (Specialized):**
13. Mouse control
14. IDE integration
15. Advanced accessibility features
