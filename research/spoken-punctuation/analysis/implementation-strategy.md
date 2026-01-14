# Implementation Strategy: Spoken Punctuation Commands for Whisper-based Dictation

## Overview

This document outlines the recommended approach for implementing spoken punctuation and formatting commands in a voice dictation system using Whisper/faster-whisper.

## Architecture

```
                                    +------------------+
                                    |                  |
Audio Input ---> faster-whisper ---> Raw Transcription ---> Post-Processing Pipeline ---> Final Text
                                    |                  |
                                    +------------------+
                                           |
                                           v
                              +------------------------+
                              | Post-Processing Steps: |
                              | 1. Escape handling     |
                              | 2. Punctuation cmds    |
                              | 3. Number conversion   |
                              | 4. Filler removal      |
                              | 5. Capitalization      |
                              +------------------------+
```

## Processing Pipeline Order

### Step 1: Escape/Literal Command Handling

Process escape commands FIRST to protect words that should not be converted:

```python
# "literal period" -> protect "period" from conversion
# "the word comma" -> protect "comma" from conversion
```

### Step 2: Spoken Punctuation Conversion

Convert punctuation command words to symbols:

```python
# "period" -> "."
# "comma" -> ","
# "new paragraph" -> "\n\n"
```

### Step 3: Number Word Conversion (Optional)

Convert spoken numbers to digits:

```python
# "twenty three" -> "23"
# "one two three" -> "123" (sequential digits)
```

### Step 4: Filler Word Removal

Remove disfluencies and filler words:

```python
# "um", "uh", "like", "you know" -> removed
```

### Step 5: Capitalization Correction

Fix capitalization based on punctuation:

```python
# ". the" -> ". The"
# "\n\n the" -> "\n\n The"
```

## Command Reference

### Punctuation Commands (Priority Order)

Process longer/more specific commands first to avoid partial matches:

```python
PUNCTUATION_COMMANDS = [
    # Multi-word commands first (longer matches)
    ("exclamation point", "!"),
    ("exclamation mark", "!"),
    ("question mark", "?"),
    ("open parenthesis", "("),
    ("close parenthesis", ")"),
    ("open paren", "("),
    ("close paren", ")"),
    ("open bracket", "["),
    ("close bracket", "]"),
    ("open brace", "{"),
    ("close brace", "}"),
    ("open quote", '"'),
    ("close quote", '"'),
    ("end quote", '"'),
    ("begin quote", '"'),
    ("new paragraph", "\n\n"),
    ("new line", "\n"),
    ("newline", "\n"),

    # Single-word commands
    ("period", "."),
    ("comma", ","),
    ("colon", ":"),
    ("semicolon", ";"),
    ("hyphen", "-"),
    ("dash", "-"),
    ("ellipsis", "..."),
    ("apostrophe", "'"),
    ("quote", '"'),
]
```

### Extended Commands (Optional)

```python
EXTENDED_COMMANDS = [
    # Currency
    ("dollar sign", "$"),
    ("percent sign", "%"),
    ("at sign", "@"),
    ("ampersand", "&"),
    ("asterisk", "*"),
    ("pound sign", "#"),
    ("hash", "#"),

    # Math
    ("plus sign", "+"),
    ("minus sign", "-"),
    ("equals sign", "="),
    ("equals", "="),

    # Special
    ("copyright sign", "(c)"),
    ("trademark sign", "(TM)"),
    ("degree sign", "deg"),
]
```

### Escape Commands

```python
ESCAPE_PREFIXES = [
    "literal",
    "the word",
    "spell out",
    "verbatim",
]
```

## Regex Patterns

### Basic Replacement Pattern

```python
import re

def create_punctuation_pattern(command):
    """Create regex pattern for a punctuation command."""
    # Match command as whole word, case-insensitive
    # Handle optional surrounding spaces appropriately
    return re.compile(
        rf'(?<!\S){re.escape(command)}(?!\S)',
        re.IGNORECASE
    )
```

### Space Handling Rules

Different punctuation types require different spacing:

```python
SPACING_RULES = {
    # No space before, space after
    "no_space_before": [".", ",", "!", "?", ":", ";", ")", "]", "}", '"'],

    # Space before, no space after
    "no_space_after": ["(", "[", "{", '"'],

    # Replace with no surrounding spaces
    "no_spaces": ["\n", "\n\n"],

    # Attach to previous word
    "attach_previous": ["'"],
}
```

### Implementation

```python
def apply_punctuation(text, command, symbol):
    """Replace command with symbol and handle spacing."""
    # Pattern matches command with surrounding context
    pattern = rf'(\s*){re.escape(command)}(\s*)'

    def replacer(match):
        before_space = match.group(1)
        after_space = match.group(2)

        # Determine spacing based on symbol type
        if symbol in [".", ",", "!", "?", ":", ";", ")", "]", "}"]:
            return symbol + " "
        elif symbol in ["(", "[", "{"]:
            return " " + symbol
        elif symbol in ["\n", "\n\n"]:
            return symbol
        elif symbol == '"':
            # Context-dependent: check if opening or closing
            return symbol
        else:
            return symbol

    return re.sub(pattern, replacer, text, flags=re.IGNORECASE)
```

## Integration with faster-whisper

### Basic Integration

```python
from faster_whisper import WhisperModel
from punctuation_processor import PunctuationProcessor

# Initialize
model = WhisperModel("base", device="cpu", compute_type="int8")
processor = PunctuationProcessor()

def transcribe_with_punctuation(audio_path):
    # Get raw transcription
    segments, info = model.transcribe(audio_path)
    raw_text = " ".join([segment.text for segment in segments])

    # Apply post-processing
    processed_text = processor.process(raw_text)

    return processed_text
```

### Real-time Integration

```python
def transcribe_realtime(audio_chunk, processor):
    """Process audio chunk with punctuation commands."""
    segments, _ = model.transcribe(audio_chunk)
    raw_text = " ".join([s.text for s in segments])

    # Process punctuation
    processed = processor.process(raw_text)

    return processed
```

## Configuration Options

### Customizable Processor

```python
processor = PunctuationProcessor(
    # Enable/disable features
    convert_punctuation=True,
    convert_numbers=True,
    remove_fillers=True,
    fix_capitalization=True,

    # Custom commands
    custom_commands=[
        ("smiley face", ":)"),
        ("sad face", ":("),
    ],

    # Escape prefix
    escape_prefix="literal",

    # Filler words to remove
    filler_words=["um", "uh", "like", "you know"],
)
```

## Testing Strategy

### Unit Tests

```python
def test_basic_punctuation():
    processor = PunctuationProcessor()

    assert processor.process("hello period") == "Hello."
    assert processor.process("how are you question mark") == "How are you?"
    assert processor.process("one comma two comma three") == "One, two, three."

def test_escape_command():
    processor = PunctuationProcessor()

    assert processor.process("the literal period of time") == "The period of time."
    assert processor.process("say the word comma not punctuation") == "Say comma not punctuation."

def test_capitalization():
    processor = PunctuationProcessor()

    assert processor.process("hello period how are you") == "Hello. How are you."
```

### Integration Tests

```python
def test_full_pipeline():
    processor = PunctuationProcessor()

    input_text = "um hello period how are you question mark i am fine comma thanks exclamation point"
    expected = "Hello. How are you? I am fine, thanks!"

    assert processor.process(input_text) == expected
```

## Performance Considerations

### Optimization Tips

1. **Compile regex patterns once** at initialization, not per-call
2. **Process commands in length order** (longest first) to avoid partial matches
3. **Use string methods** where possible (faster than regex for simple cases)
4. **Batch processing** for large texts

### Benchmarks

Typical processing times on modern hardware:

| Text Length | Processing Time |
|-------------|-----------------|
| 100 words | < 1ms |
| 1000 words | ~5ms |
| 10000 words | ~50ms |

## Error Handling

```python
class PunctuationProcessor:
    def process(self, text):
        if not text or not isinstance(text, str):
            return ""

        try:
            text = self._handle_escapes(text)
            text = self._convert_punctuation(text)
            text = self._convert_numbers(text)
            text = self._remove_fillers(text)
            text = self._fix_capitalization(text)
            text = self._clean_whitespace(text)
            return text
        except Exception as e:
            # Log error and return original text
            logger.error(f"Punctuation processing error: {e}")
            return text
```

## Deployment Recommendations

1. **Start simple:** Begin with basic punctuation commands only
2. **Add incrementally:** Add number conversion and extended commands based on user needs
3. **Monitor edge cases:** Log unexpected inputs for continuous improvement
4. **User feedback:** Allow users to report when commands don't work as expected
5. **Language support:** Consider i18n for non-English users
