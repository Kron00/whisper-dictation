# Research Sources

## Whisper and faster-whisper

### OpenAI Community Discussions

- [Whisper's auto-punctuation](https://community.openai.com/t/whispers-auto-punctuation/806764)
  - Discussion of Whisper's inconsistent handling of spoken punctuation words
  - Key finding: Whisper sometimes converts "comma" to "," which is problematic

- [Whisper: how to output punctuation as punctuation](https://community.openai.com/t/whisper-how-do-i-make-the-model-output-punctuation-as-punctuation-rather-than-transcribing-the-words/669379)
  - Users asking for Google VTT-like behavior
  - Confirmation that Whisper doesn't support this natively

- [Force no punctuation](https://github.com/openai/whisper/discussions/589)
  - Discussion of suppressing punctuation tokens
  - Useful for implementing custom punctuation handling

### OpenAI Cookbook

- [Enhancing Whisper transcriptions: pre- & post-processing techniques](https://cookbook.openai.com/examples/whisper_processing_guide)
  - Official guide to improving transcription quality
  - Covers post-processing for punctuation and terminology correction

### Academic Research

- [Evaluating OpenAI's Whisper ASR for Punctuation](https://arxiv.org/abs/2305.14580)
  - Research paper on Whisper's punctuation capabilities
  - Finding: Whisper struggles with semicolons and colons

### faster-whisper Specific

- [Disfluencies and filler words in faster-whisper](https://github.com/SYSTRAN/faster-whisper/discussions/569)
  - Discussion of filler word handling
  - Mentions post-processing approaches

---

## Commercial Dictation Systems

### Dragon NaturallySpeaking

- [Dragon Professional Individual Command Cheat Sheet (PDF)](https://www.nuance.com/asset/en_us/collateral/dragon/command-cheat-sheet/ct-dragon-professional-individual-en-us.pdf)
  - Official Nuance documentation
  - Complete list of punctuation and formatting commands

- [Dictating punctuation and symbols - Nuance Help](https://www.nuance.com/products/help/dragon/dragon-for-mac/enx/Content/Dictating/Dictating_punctuation.htm)
  - Documentation for Dragon for Mac
  - Detailed punctuation dictation guide

- [Dragon NaturallySpeaking User Guide (PDF)](https://dsp.sa.ucsb.edu/sites/default/files/2020-07/dragon_naturally_user_guide.pdf)
  - Comprehensive user manual
  - Training and punctuation sections

- [Complete list of Dragon voice commands - Philips SpeechLive](https://www.speechlive.com/us/blog/dragon-voice-commands/)
  - Third-party comprehensive command reference

### macOS Dictation

- [Commands for dictating text on Mac - Apple Support](https://support.apple.com/guide/mac-help/commands-for-dictating-text-on-mac-mh40695/mac)
  - **Official Apple documentation**
  - Complete list of punctuation, formatting, and capitalization commands

- [Dictate messages and documents on Mac - Apple Support](https://support.apple.com/guide/mac-help/use-dictation-mh40584/mac)
  - General dictation guide
  - Auto-punctuation settings

- [Use Voice Control on your Mac - Apple Support](https://support.apple.com/en-us/102225)
  - Advanced voice control features
  - Beyond basic dictation

- [How to escape punctuation in Dictation - Apple Discussions](https://discussions.apple.com/thread/8154295)
  - User discussion of literal command limitations
  - Workarounds for typing punctuation words

### Windows Voice Typing

- [Windows Speech Recognition commands - Microsoft Support](https://support.microsoft.com/en-us/windows/windows-speech-recognition-commands-9d25ef36-994d-f367-a81a-a326160128c7)
  - Official Microsoft documentation
  - Complete command reference

- [Use voice typing to talk instead of type - Microsoft Support](https://support.microsoft.com/en-us/windows/use-voice-typing-to-talk-instead-of-type-on-your-pc-fec94565-c4bd-329d-e59a-af033fa5689f)
  - Windows 11 voice typing guide
  - Auto-punctuation settings

- [Windows 11 Dictation: A Comprehensive Guide](https://texttospeech.live/blog/windows-11-dictation)
  - Third-party comprehensive guide
  - Voice Access vs. Voice Typing comparison

---

## Python Libraries

### word2number

- [word2number on PyPI](https://pypi.org/project/word2number/)
  - Convert number words to digits
  - pip install word2number

- [GitHub: akshaynagpal/w2n](https://github.com/akshaynagpal/w2n)
  - Source repository
  - Usage examples

### NVIDIA NeMo (Punctuation and Capitalization)

- [Punctuation and Capitalization Model - NVIDIA NeMo Documentation](https://docs.nvidia.com/nemo-framework/user-guide/24.07/nemotoolkit/nlp/punctuation_and_capitalization.html)
  - ML-based punctuation restoration
  - Pre-trained models available

- [NeMo Punctuation Tutorial (Jupyter Notebook)](https://github.com/NVIDIA/NeMo/blob/main/tutorials/nlp/Punctuation_and_Capitalization.ipynb)
  - Hands-on tutorial
  - Code examples

### Punctuator

- [GitHub: ottokart/punctuator](https://github.com/ottokart/punctuator)
  - LSTM RNN for punctuation restoration
  - Two-stage training approach

### Voice Command Frameworks

- [GitHub: dictation-toolbox/dragonfly](https://github.com/dictation-toolbox/dragonfly)
  - Python speech recognition framework
  - Works with Dragon, WSR, Kaldi

- [GitHub: dictation-toolbox/Caster](https://github.com/dictation-toolbox/Caster)
  - Dragonfly-based voice programming toolkit
  - Universal navigation and editing commands

- [GitHub: ideasman42/nerd-dictation](https://github.com/ideasman42/nerd-dictation)
  - Simple offline speech-to-text
  - User configuration for custom processing

### RealtimeSTT

- [GitHub: KoljaB/RealtimeSTT](https://github.com/KoljaB/RealtimeSTT)
  - Real-time speech-to-text library
  - Has ensure_sentence_ends_with_period parameter

---

## General Voice Dictation Resources

- [Voice Typing Tips and Tricks](https://www.voicetotextonline.com/voice-typing-tips-and-tricks)
  - Best practices for dictation
  - Punctuation command usage

- [How to Use Punctuation Commands in Voice Dictation - Vomo](https://vomo.ai/blog/how-to-use-punctuation-commands-in-voice-dictation)
  - Cross-platform punctuation guide
  - Common commands reference

- [What punctuation commands does dictation support? - Transcribe](https://transcribe.wreally.com/article/what-punctuation-commands-does-dictation-support-61)
  - Service-specific documentation
  - Useful command list

---

## Number Processing

- [Convert number words to integers - Stack Overflow](https://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers)
  - Python implementations
  - text2int function variations

- [IBM Speech-to-Text smart_formatting](https://www.ibm.com/support/pages/how-can-you-program-speech-text-service-output-numerical-characters-instead-spelling-out-numbers)
  - IBM's approach to number formatting
  - Smart formatting parameter documentation
