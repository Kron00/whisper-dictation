# Comprehensive Voice Dictation Feature List

This document catalogs features from major voice dictation tools that could enhance a local Linux dictation system.

---

## 1. TEXT PROCESSING & AI FEATURES

### 1.1 LLM Post-Processing
**Source:** Wispr Flow, Superwhisper, OpenAI Cookbook
**Description:** Use a local LLM to clean up raw transcription output:
- Fix grammar and punctuation errors
- Remove false starts and repetitions
- Correct homophones based on context
- Apply consistent capitalization
- Format numbers, dates, and abbreviations appropriately

**Implementation:** Can use local models like Llama 3, Mistral, or DeepSeek via Ollama. The OpenAI Cookbook documents combining Whisper with GPT-4 for post-processing; the same approach works with local LLMs.

**Why Useful:** Raw Whisper output often has minor errors. A quick LLM pass can significantly improve quality without adding much latency on modern hardware.

---

### 1.2 Context-Aware Formatting
**Source:** Wispr Flow, Willow Voice
**Description:** Automatically adjust formatting based on the active application:
- **Email apps:** Formal tone, proper salutations
- **Chat apps (Slack, Discord):** Casual, shorter sentences
- **IDEs/Terminals:** Code-aware formatting, no auto-capitalization
- **Note apps:** Bullet points, markdown formatting
- **Word processors:** Full sentences, proper punctuation

**Implementation:** Detect active window using `xdotool getwindowfocus getwindowname` or similar, then apply different post-processing prompts per application.

**Why Useful:** Speaking "new line import numpy as np" should produce different output in VS Code vs. Gmail.

---

### 1.3 Automatic Punctuation
**Source:** All major tools
**Description:** Automatically insert periods, commas, question marks based on speech patterns and pauses. Most tools now do this by default.

**Implementation:** Whisper already handles basic punctuation. Can be enhanced with LLM post-processing for edge cases.

**Why Useful:** Eliminates need to say "period" and "comma" constantly.

---

### 1.4 Smart Capitalization
**Source:** Dragon, macOS Dictation
**Description:** Automatically capitalize:
- First word of sentences
- Proper nouns (names, places, brands)
- Acronyms
- The word "I"

**Implementation:** Can be rule-based or LLM-enhanced. A custom vocabulary helps with unusual proper nouns.

**Why Useful:** Reduces post-editing time significantly.

---

## 2. VOCABULARY & PERSONALIZATION

### 2.1 Custom Vocabulary / Personal Dictionary
**Source:** Dragon, Wispr Flow, Superwhisper, Voice Gecko
**Description:** Add custom words, names, technical terms, and acronyms that the default model might not recognize:
- Medical/legal/technical terminology
- Names of people, companies, products
- Custom spellings (vs default homophones)
- Abbreviations and their expansions

**Implementation Options:**
1. **Whisper prompt parameter:** Pass a list of expected words/phrases to bias recognition
2. **Post-processing word list:** LLM corrects specific terms using a provided list
3. **Pronunciation training:** Record how you say each custom word (Dragon's approach)

**Why Useful:** Domain-specific terms are often misrecognized. "kubectl" might become "cube cuttle" without training.

---

### 2.2 Auto-Learning Vocabulary
**Source:** Wispr Flow (beta feature)
**Description:** System automatically learns new words from your typing and adds them to the vocabulary over time.

**Implementation:** Monitor clipboard/typed text for unknown words, prompt user to confirm additions.

**Why Useful:** Reduces manual dictionary maintenance.

---

### 2.3 Homophones Selection
**Source:** Talon, Dragon
**Description:** When multiple words sound the same (their/there/they're, to/two/too), provide a quick way to select the correct one.

**Implementation:** Show a quick popup or use number shortcuts when homophones are detected.

**Why Useful:** Faster than correcting manually after the fact.

---

## 3. VOICE COMMANDS & EDITING

### 3.1 Undo/Redo Commands
**Source:** All major tools
**Description:** Voice commands to undo recent dictation:
- "Undo that" - Delete last phrase/sentence
- "Undo" - Standard undo
- "Redo that" - Restore undone text
- "Scratch that" - Alternative to undo

**Implementation:** Track dictation history, implement as special command detection before/after transcription.

**Why Useful:** Critical for maintaining flow without reaching for keyboard.

---

### 3.2 Text Selection Commands
**Source:** Dragon, macOS Voice Control, Windows Voice Access
**Description:** Select text by voice:
- "Select [word/phrase]"
- "Select last sentence"
- "Select paragraph"
- "Select all"
- "Select from [x] to [y]"

**Implementation:** Parse commands, use xdotool or ydotool to execute selections.

**Why Useful:** Enables complete hands-free editing workflow.

---

### 3.3 Text Deletion Commands
**Source:** All major tools
**Description:** Delete specific text:
- "Delete that" - Delete selection or last phrase
- "Delete [word/phrase]"
- "Delete last [n] words"
- "Delete line"
- "Backspace [n]"

**Implementation:** Track context, execute appropriate delete operations.

**Why Useful:** Faster corrections without keyboard.

---

### 3.4 Text Manipulation Commands
**Source:** Google Docs, Microsoft Voice Access
**Description:** Transform selected or recent text:
- "Make that uppercase/lowercase"
- "Capitalize that"
- "Bold that" / "Italicize that"
- "Make that a list"
- "Format as code"

**Implementation:** Detect commands, apply formatting (may be app-specific).

**Why Useful:** Complex formatting without mouse clicks.

---

### 3.5 Navigation Commands
**Source:** Dragon, macOS Voice Control
**Description:** Move cursor by voice:
- "Go to beginning/end"
- "Go to line [n]"
- "Move up/down [n] lines"
- "Next/previous word"
- "Next/previous paragraph"

**Implementation:** Map commands to keyboard shortcuts.

**Why Useful:** Complete document navigation without touching keyboard.

---

### 3.6 Insert/Replace Commands
**Source:** Google Gboard, Windows Voice Access
**Description:** Precise text insertion:
- "Insert [text] before [word]"
- "Insert [text] after [word]"
- "Replace [old] with [new]"

**Implementation:** Parse command structure, locate target, perform edit.

**Why Useful:** Surgical edits without manual cursor positioning.

---

## 4. SNIPPETS & TEMPLATES

### 4.1 Voice-Triggered Snippets
**Source:** Wispr Flow, Dragon, VoiceMacro
**Description:** Speak a short trigger phrase to insert longer pre-defined text:
- "Insert signature" -> Full email signature
- "Insert address" -> Complete mailing address
- "Standard greeting" -> "Thank you for your email..."
- Custom code blocks, boilerplate text

**Implementation:** Maintain snippet database, detect trigger phrases, insert expansion.

**Why Useful:** Massive time saver for repetitive text.

---

### 4.2 Dynamic Templates with Variables
**Source:** Dragon Professional, Text Blaze
**Description:** Snippets with placeholders that prompt for values:
- "New email to [name]" -> Template with name inserted
- "Meeting notes for [date]" -> Formatted template with date

**Implementation:** Parse variables from template, prompt or auto-fill based on context.

**Why Useful:** Structured documents with voice.

---

### 4.3 Application-Specific Snippets
**Source:** Dragon Professional
**Description:** Different snippet libraries for different applications. "Insert header" does different things in code vs. documents.

**Implementation:** Associate snippet sets with window class/name patterns.

**Why Useful:** Same voice command, context-appropriate results.

---

## 5. LANGUAGE & LOCALIZATION

### 5.1 Multi-Language Support
**Source:** Wispr Flow (100+ languages), Superwhisper, Whisper
**Description:** Transcribe in languages other than English.

**Implementation:** Whisper natively supports 99 languages. Select language in config or per-session.

**Why Useful:** Essential for non-English users or multilingual content.

---

### 5.2 Automatic Language Detection
**Source:** Wispr Flow, Superwhisper, dictop
**Description:** Automatically detect and switch between languages without manual selection.

**Implementation:** Whisper supports language detection. Can also use a short initial sample to detect before full transcription.

**Why Useful:** Seamless for multilingual users or mixed-language content.

---

### 5.3 Code-Switching Support
**Source:** NVIDIA NeMo research
**Description:** Handle switching between languages within the same utterance (common for bilingual speakers).

**Implementation:** Requires models trained on code-switched data. Whisper handles this reasonably well.

**Why Useful:** Natural speech for bilingual users often mixes languages.

---

## 6. AUDIO & INPUT HANDLING

### 6.1 Multiple Microphone Profiles
**Source:** Dragon Professional
**Description:** Save different settings for different microphones (laptop mic, headset, USB mic) with per-device calibration.

**Implementation:** Detect audio device, load corresponding profile with gain, noise settings.

**Why Useful:** Optimal recognition regardless of which mic is in use.

---

### 6.2 Noise Reduction / Echo Cancellation
**Source:** Dragon, Picovoice
**Description:** Pre-process audio to remove:
- Background noise (fans, AC, traffic)
- Echo from speakers
- Keyboard clicks
- Other voices in background

**Implementation:** Use RNNoise, PulseAudio noise suppression, or similar. WebRTC VAD for voice activity detection.

**Why Useful:** Better recognition accuracy in non-ideal environments.

---

### 6.3 Audio Recording / Playback
**Source:** Dragon, Microsoft Word Transcribe
**Description:** Save audio alongside transcription for later review. Play back specific sections.

**Implementation:** Save audio buffer to file with timestamps. Allow playback synced to transcript.

**Why Useful:** Verify uncertain transcriptions, create meeting records.

---

### 6.4 Variable Speed Playback
**Source:** Voice recorders, transcription tools
**Description:** Play back recordings at 0.5x to 2x speed for review.

**Implementation:** Use audio processing library to adjust playback speed.

**Why Useful:** Faster review of long recordings.

---

## 7. USER INTERFACE & ACTIVATION

### 7.1 Wake Word Activation
**Source:** Picovoice Porcupine, Home Assistant, Alexa/Siri
**Description:** Always-listening for a trigger phrase like "Hey Computer" or custom wake word.

**Implementation:** Use Picovoice Porcupine (has Linux support) or similar for low-resource wake word detection. Only activates main recognition when triggered.

**Why Useful:** Completely hands-free activation.

---

### 7.2 Configurable Hotkeys
**Source:** All tools
**Description:** User-defined keyboard shortcuts for:
- Start/stop recording
- Toggle modes
- Cancel current dictation
- Quick correction mode

**Implementation:** Global hotkey listener with user configuration.

**Why Useful:** Flexibility for different workflows and preferences.

---

### 7.3 System Tray / Status Indicator
**Source:** Superwhisper, Wispr Flow
**Description:** Visual indicator showing:
- Ready/recording/processing state
- Current mode
- Quick access to settings
- Recent dictations

**Implementation:** System tray icon with context menu and state changes.

**Why Useful:** Immediate visual feedback without dedicated window.

---

### 7.4 Floating Dictation Bar
**Source:** Dragon, Wispr Flow
**Description:** Small floating window showing real-time transcription that follows cursor or stays in fixed position.

**Implementation:** Overlay window with streaming text display.

**Why Useful:** Visual feedback while dictating, especially helpful for longer content.

---

### 7.5 Dictation History
**Source:** Superwhisper, Alter
**Description:** Searchable history of all dictations:
- Timestamp and application context
- One-click to copy previous dictation
- Search by content
- Statistics over time

**Implementation:** SQLite database of dictations with metadata.

**Why Useful:** Never lose dictated content, easy reuse of previous text.

---

## 8. PRODUCTIVITY & WORKFLOW

### 8.1 Statistics and Analytics
**Source:** Wispr Flow, writing apps
**Description:** Track and display:
- Words dictated per day/week/month
- Time saved vs typing
- Most common corrections
- Accuracy trends
- Streaks and achievements

**Implementation:** Log dictation events, build dashboard or periodic reports.

**Why Useful:** Motivation, identify areas for improvement.

---

### 8.2 Clipboard Integration
**Source:** Superwhisper, Voice Notebook
**Description:** Options for where dictated text goes:
- Paste directly to cursor (current behavior)
- Copy to clipboard only (no paste)
- Both (paste and keep in clipboard)
- Append to clipboard history

**Implementation:** Configuration option for output behavior.

**Why Useful:** Flexibility for different workflows, integration with clipboard managers.

---

### 8.3 Queue Mode / Batch Dictation
**Source:** Dragon Professional
**Description:** Dictate multiple separate items that get processed and stored, then insert them one by one.

**Implementation:** Buffer system with review before insertion.

**Why Useful:** Prepare multiple responses/items without switching context.

---

## 9. MOUSE & SYSTEM CONTROL

### 9.1 Voice-Controlled Mouse
**Source:** macOS Voice Control, Windows Voice Access, Talon
**Description:** Control mouse cursor by voice:
- "Mouse up/down/left/right [amount]"
- Grid overlay with numbered zones
- "Click" / "Double click" / "Right click"
- "Drag from [x] to [y]"

**Implementation:** Grid overlay system or directional commands via xdotool/ydotool.

**Why Useful:** Complete hands-free operation for accessibility or RSI.

---

### 9.2 Scrolling Commands
**Source:** All major tools
**Description:** Scroll documents by voice:
- "Scroll up/down"
- "Page up/down"
- "Scroll to top/bottom"

**Implementation:** Send scroll key events.

**Why Useful:** Document navigation without touching mouse.

---

### 9.3 Application Control
**Source:** Windows Voice Access, macOS Voice Control, Talon
**Description:** Control applications by voice:
- "Open [app name]"
- "Close window"
- "Switch to [app]"
- "Minimize" / "Maximize"
- "New tab" / "Close tab"

**Implementation:** D-Bus commands, xdotool, or application-specific commands.

**Why Useful:** Complete system control by voice.

---

### 9.4 Pop/Hiss Sounds as Commands
**Source:** Talon
**Description:** Use non-speech sounds as shortcuts:
- Pop sound -> Click
- Hiss sound -> Scroll
- Whistle -> Custom action

**Implementation:** Train audio classifier for specific sounds.

**Why Useful:** Faster than speaking commands for common actions.

---

## 10. CODING-SPECIFIC FEATURES

### 10.1 IDE Integration
**Source:** VS Code Speech, Wispr Flow, Serenade, Talon
**Description:** Deep integration with code editors:
- "Go to line 42"
- "Go to definition"
- "Find references"
- "Run tests"
- "Open file [name]"
- Copilot/AI integration via voice

**Implementation:** VS Code extension API, LSP integration, or simulating keyboard shortcuts.

**Why Useful:** Voice-first development workflow.

---

### 10.2 Symbol Dictation
**Source:** Talon, Serenade
**Description:** Easy dictation of programming symbols:
- "op equals" -> =
- "double equals" -> ==
- "arrow" -> ->
- "fat arrow" -> =>
- "open paren" -> (
- "string [text]" -> "[text]"

**Implementation:** Symbol vocabulary with context-aware expansion.

**Why Useful:** Code is full of symbols that are awkward to dictate literally.

---

### 10.3 Code Navigation with Hats (Cursorless)
**Source:** Talon + Cursorless
**Description:** Visual markers ("hats") on code elements that can be referenced by voice for selection, deletion, or manipulation.

**Implementation:** VS Code extension that adds visual markers and responds to voice commands.

**Why Useful:** Extremely efficient code editing by voice.

---

### 10.4 Language-Specific Commands
**Source:** Talon community
**Description:** Programming language-aware commands:
- "define function [name]" -> language-appropriate syntax
- "for loop" -> language-appropriate for syntax
- "import [module]" -> correct import statement

**Implementation:** Language detection + template library per language.

**Why Useful:** Write idiomatic code without dictating every character.

---

## 11. ACCESSIBILITY FEATURES

### 11.1 Adjustable Speaking Speed/Timeout
**Source:** Various
**Description:** Configure how fast/slow users can speak and how long to wait before considering utterance complete.

**Implementation:** Configurable VAD parameters, longer/shorter silence detection.

**Why Useful:** Accommodates different speaking styles and speech impediments.

---

### 11.2 Visual Feedback for Deaf/HoH Users
**Source:** Accessibility guidelines
**Description:** All audio feedback should have visual alternatives. Sound indicators should be accompanied by visual state changes.

**Implementation:** Ensure all states are reflected in UI, not just sounds.

**Why Useful:** Inclusive design for users who may not hear audio cues.

---

### 11.3 Repeat Last Command
**Source:** Various
**Description:** "Repeat that" to execute the last command or dictation again.

**Implementation:** Track last action, implement repeat command.

**Why Useful:** Reduces need to re-dictate for repetitive tasks.

---

## 12. PRIVACY & SECURITY

### 12.1 On-Device Processing
**Source:** Superwhisper, Apple Dictation, Dragon
**Description:** All processing happens locally, no audio or text sent to cloud servers.

**Implementation:** Already using faster-whisper locally. Ensure any LLM post-processing also uses local models.

**Why Useful:** Privacy, offline operation, no subscription costs.

---

### 12.2 Privacy Mode / Sensitive App Detection
**Source:** Wispr Flow Enterprise
**Description:** Automatically pause or disable dictation when certain applications are in focus (banking, password managers).

**Implementation:** Window class/name blocklist that prevents recording.

**Why Useful:** Prevent accidental capture of sensitive information.

---

### 12.3 Encrypted Dictation History
**Source:** Enterprise tools
**Description:** If storing dictation history locally, encrypt it at rest.

**Implementation:** SQLite encryption or encrypted filesystem.

**Why Useful:** Protect potentially sensitive dictated content.

---
