# Main Research Findings: Spoken Punctuation in Voice Dictation

## 1. Does Whisper/faster-whisper Have Built-in Support?

**Answer: No**

Whisper and faster-whisper do NOT natively support spoken punctuation commands. The model's behavior is inconsistent:

- Sometimes Whisper replaces "comma" with "," automatically (problematic because you can't tell if it was spoken or auto-inserted)
- Other times it transcribes the words literally: "This is the list colon newline dash..."
- The behavior depends on context, model size, and audio characteristics

**Key quote from OpenAI community:** "Since Whisper is not instruction-tuned, it's difficult to make it consistently interpret spoken punctuation as commands."

### What Whisper DOES Do

Whisper has **auto-punctuation** that:
- Automatically adds commas, periods, and question marks based on speech patterns
- Automatically handles capitalization
- Sometimes gets stuck in a "no-punctuation mode" for long audio

This is different from **spoken punctuation commands** where the user explicitly says "period" to insert a period.

### Potential Workarounds in Whisper

1. **Suppress punctuation tokens** during decoding, then handle ALL punctuation in post-processing
2. **Use initial prompt** to encourage punctuation mode: `"Hello, welcome to my lecture."`
3. **Post-process** to convert spoken punctuation words to symbols (recommended approach)

## 2. How Do Commercial Dictation Systems Handle This?

All major systems handle this through dedicated command processing, not the speech model:

### Dragon NaturallySpeaking
- Most comprehensive punctuation command support
- Supports complex commands like "Put quotes around that"
- Natural Punctuation feature for automatic insertion
- User tip: "Pause before and after commands but not within them"

### macOS Dictation
- Full punctuation command support (period, comma, question mark, etc.)
- Formatting commands (new line, new paragraph, tab key)
- Capitalization control (caps on/off, all caps)
- Special feature: "numeral" command to format as numbers
- Auto-punctuation can be disabled in System Settings

### Windows Voice Typing / Voice Access
- Standard punctuation commands supported
- Auto-punctuation available (off by default)
- Can say "Type" or "Dictate" before words to insert them literally
- Voice Access replaced Windows Speech Recognition in September 2024

## 3. Best Approach for Post-Processing Implementation

### Recommended Architecture

```
Audio -> Whisper/faster-whisper -> Raw Text -> Post-Processing Pipeline -> Final Text
```

### Post-Processing Pipeline Order

1. **Spoken punctuation conversion** (FIRST - before other processing)
2. **Number word to digit conversion** (optional)
3. **Filler word removal** (after punctuation to avoid conflicts)
4. **Capitalization correction** (last, based on final punctuation)

### Why This Order Matters

- Punctuation commands should be processed first because:
  - Filler word lists might accidentally match punctuation words
  - Capitalization depends on knowing where sentences end
  - Number processing might need to know sentence boundaries

## 4. Python Libraries for This Task

### No Dedicated Library Exists

There is no specific Python library for converting spoken punctuation to symbols. Custom implementation is required.

### Related Libraries

| Library | Purpose | Notes |
|---------|---------|-------|
| `word2number` | Convert "twenty one" to 21 | Pip installable, works well |
| `nemo` (NVIDIA) | Add punctuation/capitalization | ML-based, for missing punctuation |
| `punctuator` | Restore missing punctuation | LSTM-based, trained model |
| `dragonfly` | Voice command framework | Full framework, overkill for this |
| `nerd-dictation` | Offline dictation | Has config hook for custom processing |

### Key Library: word2number

```python
from word2number import w2n

w2n.word_to_num("twenty one")  # Returns: 21
w2n.word_to_num("two point three")  # Returns: 2.3
```

## 5. Processing Order: Before or After Filler Word Removal?

**Answer: BEFORE filler word removal**

### Rationale

1. **Avoid false positives:** A word like "um" in filler list won't conflict with punctuation commands, but processing order ensures clean boundaries

2. **Context preservation:** Punctuation commands often come at natural pause points where fillers also occur. Processing punctuation first maintains cleaner sentence boundaries.

3. **Capitalization dependency:** After converting "period" to ".", the next word should be capitalized. This is easier if punctuation is resolved first.

### Recommended Pipeline

```python
def process_transcription(text):
    # Step 1: Convert spoken punctuation to symbols
    text = convert_punctuation_commands(text)

    # Step 2: Convert number words (optional)
    text = convert_number_words(text)

    # Step 3: Remove filler words
    text = remove_filler_words(text)

    # Step 4: Fix capitalization after punctuation
    text = fix_capitalization(text)

    return text
```

## 6. Edge Cases: User Wants the Word "Period" in Their Text

### Solutions Used by Commercial Systems

1. **"Literal" command (macOS):** Say "literal period" to insert the word "period"
   - Note: This is inconsistent for punctuation words in macOS

2. **"Type/Dictate" prefix (Windows):** Say "Type period" to insert "period"

3. **"Spell" command:** Spell out P-E-R-I-O-D

4. **Context detection:** Smart systems detect context like "the period of history" vs "end of sentence period"

### Recommended Implementation

```python
ESCAPE_WORDS = ["literal", "spell out", "the word"]

def process_with_escape(text):
    # Handle "literal comma" -> "comma"
    for escape in ESCAPE_WORDS:
        pattern = rf'{escape}\s+(\w+)'
        text = re.sub(pattern, r'\1', text, flags=re.IGNORECASE)

    # Then process remaining punctuation commands
    return convert_punctuation_commands(text)
```

## 7. Number Handling: "One Two Three" -> "123" or "1 2 3"?

### The Challenge

The same spoken input can have multiple valid interpretations:
- "one two three" could be: "123" (sequence) or "1 2 3" (separate digits)
- "twenty three" should be: "23" (not "20 3")

### Commercial System Approaches

- **IBM Speech-to-Text:** Has `smart_formatting` parameter for phone numbers, dates
- **Dragon:** Context-aware number formatting
- **macOS:** "Numeral" command forces number format

### Recommended Implementation

```python
# Default: Compound numbers are summed
"twenty three" -> 23

# Sequential single digits become a sequence
"one two three" -> "123"

# Use "numeral" prefix for explicit number mode
"numeral five five five" -> "555"

# Use spaces with "space" command
"one space two space three" -> "1 2 3"
```

## 8. Capitalization After Periods

### Automatic Capitalization Rules

1. Capitalize first character after: `.` `!` `?`
2. Capitalize first character after: `\n\n` (new paragraph)
3. Capitalize first character of entire text
4. Handle edge cases: `...` should not trigger capitalization

### Implementation

```python
def fix_capitalization(text):
    # Capitalize after sentence-ending punctuation
    text = re.sub(
        r'([.!?])\s+([a-z])',
        lambda m: m.group(1) + ' ' + m.group(2).upper(),
        text
    )

    # Capitalize after new paragraph
    text = re.sub(
        r'(\n\n)([a-z])',
        lambda m: m.group(1) + m.group(2).upper(),
        text
    )

    # Capitalize first character
    if text and text[0].islower():
        text = text[0].upper() + text[1:]

    return text
```
