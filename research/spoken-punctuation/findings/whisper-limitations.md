# Whisper/faster-whisper: Limitations and Workarounds for Spoken Punctuation

## Core Limitation

Whisper was designed as a speech-to-text transcription model, not a dictation command interpreter. It does NOT have built-in support for:

- Converting "period" to "."
- Converting "comma" to ","
- Interpreting "new line" as a line break
- Any other spoken punctuation commands

## Whisper's Actual Punctuation Behavior

### Auto-Punctuation (What Whisper DOES do)

Whisper automatically:
1. Adds periods at sentence boundaries based on prosody
2. Adds commas at clause boundaries
3. Adds question marks when it detects questioning intonation
4. Handles capitalization at sentence starts

**Limitations of auto-punctuation:**
- Struggles with semicolons and colons
- Can get stuck in "no-punctuation mode" on long audio
- Exclamation marks are sometimes missed
- Behavior varies by model size

### Inconsistent Handling of Spoken Punctuation Words

When users say punctuation words, Whisper's behavior is unpredictable:

```
Input audio: "Hello comma how are you question mark"

Possible outputs:
1. "Hello, how are you?"        <- Sometimes converts (inconsistent)
2. "Hello comma how are you question mark"  <- Sometimes literal
3. "Hello, how are you question mark"       <- Sometimes mixed
```

This inconsistency makes it unusable for reliable dictation without post-processing.

## Why Whisper Doesn't Support Spoken Punctuation Commands

1. **Training data:** Whisper was trained on web audio (podcasts, YouTube, etc.) where people don't typically say "period" to mean punctuation

2. **Not instruction-tuned:** Unlike GPT models, Whisper doesn't follow instructions or interpret commands

3. **Design goal:** Whisper aims for accurate transcription of what was said, not interpretation of what was meant

## Workarounds and Approaches

### Approach 1: Post-Processing (Recommended)

Process Whisper output to convert punctuation words to symbols:

```python
import faster_whisper

model = WhisperModel("base")
segments, info = model.transcribe("audio.wav")
text = " ".join([segment.text for segment in segments])

# Post-process
text = convert_punctuation_commands(text)
```

**Pros:**
- Full control over command set
- Consistent behavior
- Can add custom commands

**Cons:**
- May have false positives (rare with good patterns)
- Additional processing step

### Approach 2: Suppress All Punctuation in Whisper

Configure Whisper to suppress punctuation tokens, then add all punctuation in post-processing:

```python
# Suppress common punctuation tokens
# Note: Token IDs vary by model
suppress_tokens = [",", ".", "!", "?", ";", ":"]

# This requires modifying decoding parameters
# faster-whisper supports suppress_tokens parameter
```

**Pros:**
- Complete control over punctuation
- No inconsistent auto-punctuation

**Cons:**
- Loses Whisper's prosody-based punctuation
- More work in post-processing
- May affect transcription quality

### Approach 3: Use Initial Prompt to Encourage Punctuation Mode

```python
from faster_whisper import WhisperModel

model = WhisperModel("base")
segments, info = model.transcribe(
    "audio.wav",
    initial_prompt="Hello, welcome to my lecture. How are you today?"
)
```

**Pros:**
- Can improve consistency of auto-punctuation
- Simple to implement

**Cons:**
- Doesn't solve spoken punctuation command problem
- Effects are subtle and inconsistent

### Approach 4: Two-Pass Transcription

1. First pass: Focus on accurate words (suppress punctuation)
2. Second pass: Focus on timestamps and prosody
3. Merge results and apply post-processing

**Pros:**
- Can optimize for both accuracy and timing

**Cons:**
- Double processing time
- Complex implementation

## Faster-Whisper Specific Options

faster-whisper provides some relevant parameters:

```python
from faster_whisper import WhisperModel

model = WhisperModel("base")
segments, info = model.transcribe(
    "audio.wav",
    word_timestamps=True,  # Get word-level timing
    vad_filter=True,       # Voice activity detection
    vad_parameters={
        "min_silence_duration_ms": 500,
    }
)
```

**word_timestamps:** Can help identify natural pauses where punctuation commands might occur

**vad_filter:** Can segment audio at silence boundaries, useful for sentence detection

## Model Size Considerations

| Model | Punctuation Accuracy | Notes |
|-------|---------------------|-------|
| tiny | Poor | Often missing punctuation |
| base | Fair | Basic punctuation works |
| small | Good | Reliable for common punctuation |
| medium | Very Good | Better with complex punctuation |
| large | Excellent | Best overall quality |
| large-v3 | Excellent | Latest improvements |

**Recommendation:** Use at least "small" model for punctuation-sensitive applications.

## Known Issues

### 1. No-Punctuation Mode
Whisper can get stuck generating unpunctuated text, especially on:
- Very long audio (>30 minutes)
- Audio with poor quality
- Audio with non-standard speech patterns

**Mitigation:** Segment audio into smaller chunks (5-10 minutes max)

### 2. Language Mixing
Non-English words or accents can disrupt punctuation detection.

**Mitigation:** Set explicit language parameter

### 3. Integer Timestamps Correlation
There's a correlation between integer timestamps and missing punctuation.

**Mitigation:** Use condition_on_previous_text=True

## Conclusion

For reliable spoken punctuation command support, **post-processing is required**. Whisper should be treated as a transcription engine, and a separate processing layer should handle:

1. Spoken punctuation command conversion
2. Custom formatting commands
3. Escape mechanisms for literal words
4. Capitalization after punctuation

This approach mirrors how commercial dictation systems work and provides the most reliable results.
