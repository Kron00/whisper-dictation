# Open Questions and Areas for Further Research

Questions and topics that emerged during research that may warrant additional investigation.

---

## TECHNICAL QUESTIONS

### 1. Optimal Command Detection Strategy
**Question:** Should voice commands be detected before or after Whisper transcription?

**Options:**
- **Pre-detection:** Use small classifier to detect command vs. dictation before sending to Whisper. Faster for commands but adds complexity.
- **Post-detection:** Send everything to Whisper, parse transcription for commands. Simpler but commands get full transcription latency.
- **Hybrid:** Quick keyword spotting for common commands, full transcription for ambiguous cases.

**Further Research:** Benchmark different approaches with real usage patterns.

---

### 2. LLM Post-Processing Trade-offs
**Question:** What's the optimal model size and when should LLM post-processing be applied?

**Considerations:**
- Always vs. on-demand (user toggle)
- Based on text length (skip for short phrases)
- Based on application context (only for formal writing)
- User-adjustable "cleanup level"

**Further Research:** User testing to find preferred defaults, latency tolerance thresholds.

---

### 3. Wake Word Resource Usage
**Question:** Is always-on wake word detection acceptable for a desktop dictation tool?

**Concerns:**
- Battery usage (less relevant for desktop)
- Privacy perception of always-listening
- False positive rate in shared spaces

**Further Research:** Evaluate Porcupine vs alternatives, test false positive rates, gather user preferences.

---

### 4. Wayland Compatibility
**Question:** What's the best approach for Wayland compatibility?

**Current State:**
- ydotool works but requires root/special permissions
- wtype works for typing but limited for control
- wlrctl for some compositors
- No universal solution

**Further Research:** Monitor wlroots and GNOME developments, test dotool as alternative.

---

### 5. Audio Pipeline Latency
**Question:** What's the minimum achievable latency for the full pipeline?

**Components:**
- Audio capture buffer size
- VAD detection time
- Whisper processing
- Command parsing
- Input simulation

**Further Research:** Profile each component, identify bottlenecks, test different buffer sizes.

---

## USER EXPERIENCE QUESTIONS

### 6. Feedback Modality Preferences
**Question:** What feedback do users prefer during dictation?

**Options:**
- Audio: Beeps, sounds
- Visual: Tray icon changes, floating window
- Haptic: (not applicable to desktop)
- Minimal: No feedback until complete

**Further Research:** Survey users, A/B test different feedback approaches.

---

### 7. Error Correction Workflow
**Question:** What's the most efficient way to handle transcription errors?

**Options:**
- Undo and re-dictate
- "Correct [word]" command
- Post-dictation review mode
- Homophones popup
- Trust LLM to fix most errors

**Further Research:** Study error patterns, user correction behaviors, time to correct.

---

### 8. Learning Curve for Voice Commands
**Question:** How many commands are practical for users to remember?

**Observations:**
- Dragon has hundreds of commands, but most users use <20
- Simple commands ("undo that") have high adoption
- Complex commands ("select from X to Y") rarely used

**Further Research:** Track command usage frequency, identify most valuable commands.

---

### 9. Context Switching Behavior
**Question:** How should the system handle rapid context switches?

**Scenarios:**
- User switches from IDE to Slack mid-dictation
- User copies text during dictation (clipboard context)
- User minimizes app, dictation continues

**Further Research:** Define expected behaviors, test edge cases.

---

## FEATURE VIABILITY QUESTIONS

### 10. Voice Coding Adoption
**Question:** Is voice coding practical for day-to-day development?

**Considerations:**
- Learning curve is significant
- Talon/Cursorless users report high productivity after training
- Not suitable for all coding tasks (debugging, reading code)

**Further Research:** Interview voice coding practitioners, document realistic expectations.

---

### 11. Multi-Language Detection Reliability
**Question:** How reliable is automatic language detection in practice?

**Concerns:**
- Short utterances may be misclassified
- Code-switching within sentences
- Accents and dialects
- Technical terms from other languages

**Further Research:** Test with real multilingual users, document failure cases.

---

### 12. Privacy vs. Cloud Quality Trade-off
**Question:** How much quality are users willing to sacrifice for privacy?

**Observations:**
- Wispr Flow (cloud) vs Superwhisper (local) quality gap is narrowing
- Whisper large-v3 approaches commercial cloud quality
- Local LLMs still lag behind GPT-4 for complex corrections

**Further Research:** Blind comparison tests, user satisfaction surveys.

---

## MARKET & ECOSYSTEM QUESTIONS

### 13. Talon Integration
**Question:** Should the system integrate with Talon rather than build parallel features?

**Considerations:**
- Talon has mature voice command infrastructure
- Large community with extensive command sets
- But: X11 only, Python 3.9, specific architecture
- Faster-whisper may have different trade-offs vs Talon's speech engine

**Further Research:** Evaluate Talon integration feasibility, compare architectures.

---

### 14. VS Code Extension Development
**Question:** Is a dedicated VS Code extension worthwhile?

**Benefits:**
- Access to VS Code APIs for navigation
- Could integrate with Copilot
- VS Code Speech extension as reference

**Costs:**
- Significant development effort
- Needs maintenance across VS Code updates
- Only benefits VS Code users

**Further Research:** Survey user base for IDE distribution, evaluate VS Code Speech API.

---

### 15. Mobile Companion App
**Question:** Would a mobile companion app (Android) add value?

**Use Cases:**
- Dictate on phone, send to desktop
- Remote control of desktop dictation
- Mobile dictation with same vocabulary

**Further Research:** User demand, technical feasibility, privacy considerations.

---

## RESEARCH GAPS

### Areas Needing More Information

1. **Benchmark comparisons:** No rigorous benchmarks comparing faster-whisper to Dragon/Wispr Flow accuracy
2. **Linux dictation surveys:** Limited data on Linux user dictation habits and preferences
3. **RSI/accessibility case studies:** How do users with disabilities use Linux dictation tools?
4. **Long-form dictation:** Most tools optimize for short phrases; less research on long-form writing
5. **Code dictation accuracy:** No standardized benchmark for code dictation accuracy

### Suggested Next Steps

1. Create benchmark suite for measuring dictation quality
2. Survey Linux dictation users on feature priorities
3. Interview Talon/Dragon power users on workflows
4. Document common transcription errors for custom vocabulary
5. Test LLM post-processing with various model sizes
6. Prototype command detection and measure latency
7. Build simple dictation history and evaluate usefulness

---

## RESOURCES FOR FURTHER RESEARCH

### Communities
- Talon Slack workspace
- r/speechrecognition subreddit
- Whisper GitHub discussions
- Dragon NaturallySpeaking forums

### Documentation
- Whisper paper and blog posts
- Talon documentation
- VS Code Speech extension source code
- Picovoice Porcupine documentation

### Academic Papers
- "Whisper: Robust Speech Recognition via Large-Scale Weak Supervision"
- Wake word detection literature
- Voice activity detection algorithms
- LLM for speech error correction
