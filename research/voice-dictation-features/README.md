# Voice Dictation Features Research

**Research Date:** December 6, 2025
**Topic:** Feature analysis of voice dictation tools for enhancing a local Linux dictation system

## Executive Summary

This research analyzes features from leading voice dictation tools (Wispr Flow, Talon, Dragon NaturallySpeaking, Superwhisper, macOS/Windows dictation, and others) to identify enhancements for a local Linux voice dictation system.

### Key Findings

1. **AI-Powered Post-Processing** - Modern tools use LLMs to clean up transcriptions, fix grammar, remove filler words, and apply context-aware formatting. This can be done locally with models like Llama or DeepSeek.

2. **Context-Aware Formatting** - Leading tools detect which application is active and adjust formatting accordingly (casual for Slack, formal for email, code-aware for IDEs).

3. **Custom Vocabulary/Dictionary** - Essential for technical terms, names, and domain-specific jargon. Dragon's approach of training pronunciation is highly effective.

4. **Voice Commands for Editing** - "Undo that", "delete last sentence", "select paragraph" - commands that edit without leaving voice mode are critical for productivity.

5. **Snippet/Template System** - Voice-triggered text expansion for frequently used phrases, signatures, code blocks, or formatted text.

## Folder Structure

```
research-voice-dictation-features/
├── README.md                    (This file)
├── findings/
│   ├── main-findings.md         (Comprehensive feature list)
│   ├── feature-comparison.md    (Tool-by-tool comparison)
│   └── implementation-priority.md (Prioritized recommendations)
├── sources/
│   └── tools-researched.md      (Source documentation)
└── analysis/
    ├── local-implementation.md  (Features practical for local use)
    └── open-questions.md        (Areas needing further research)
```

## Current System Features (Already Implemented)

- Double middle-click to start/stop recording
- GPU-accelerated transcription (faster-whisper on RTX 3090)
- Daemon architecture keeping model in VRAM
- Streaming preview (partial transcription while speaking)
- Filler word removal (um, uh, like, etc.)
- Whisper mode for quiet/low-volume speech
- Auto-pause/resume music during dictation
- Auto-paste after transcription

## Top Recommended Additions

See `findings/implementation-priority.md` for the full prioritized list. The highest-impact features are:

1. Voice editing commands (undo, delete, select)
2. Custom vocabulary/personal dictionary
3. Snippet/template system with voice triggers
4. Context-aware formatting per application
5. LLM post-processing for grammar/punctuation
6. Multi-language auto-detection
7. Dictation history with search
8. Voice-controlled mouse/navigation
9. Wake word activation option
10. Statistics and productivity tracking

## Limitations and Caveats

- Cloud-dependent features (Wispr Flow's tone matching, some LLM features) require adaptation for local use
- Some features (eye tracking) require specialized hardware
- Wayland support is limited for some Linux tools (Talon requires X11)
- Local LLM post-processing adds latency vs. cloud solutions

## Sources

Primary sources include official documentation and reviews of:
- Wispr Flow (wisprflow.ai)
- Talon Voice (talonvoice.com)
- Dragon NaturallySpeaking (nuance.com)
- Superwhisper (superwhisper.com)
- Nerd Dictation (github.com/ideasman42/nerd-dictation)
- macOS Voice Control / Dictation
- Windows 11 Voice Access
- VS Code Speech Extension
- Serenade (serenade.ai)
