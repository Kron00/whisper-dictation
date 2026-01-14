# Edge Cases and Solutions for Spoken Punctuation Processing

## 1. User Wants the Literal Word "Period"

### The Problem

When a user says "the period of history," they want the word "period," not a dot.

### Solutions

#### Solution A: Escape Command (Recommended)

Support an escape prefix like "literal" or "the word":

```python
# Input: "the literal period of history"
# Output: "the period of history"

# Input: "say the word comma not punctuation"
# Output: "say comma not punctuation"
```

#### Solution B: Context Detection

Use NLP to detect when "period" is used as a noun vs. command:

```python
# "end of sentence period" -> "end of sentence."
# "the victorian period" -> "the victorian period"  (noun usage)
```

**Challenge:** Requires NLP model, adds complexity and latency.

#### Solution C: Position-Based Heuristic

Only convert punctuation words at typical command positions:

```python
# At end of phrase: "hello period" -> "hello."
# After determiner: "the period" -> "the period" (likely noun)
```

### Recommended Implementation

```python
ESCAPE_PREFIXES = ["literal", "the word", "spell out"]

def handle_escapes(text):
    """Replace 'literal X' with a protected placeholder."""
    for prefix in ESCAPE_PREFIXES:
        # Pattern: escape_prefix + word
        pattern = rf'{prefix}\s+(\w+)'
        # Replace with placeholder that won't match punctuation patterns
        text = re.sub(pattern, r'__LITERAL_\1__', text, flags=re.IGNORECASE)
    return text

def restore_literals(text):
    """Restore protected words after punctuation processing."""
    return re.sub(r'__LITERAL_(\w+)__', r'\1', text)
```

---

## 2. Multiple Punctuation in Sequence

### The Problem

User says: "wow exclamation point exclamation point exclamation point"

### Expected Output

"Wow!!!"

### Implementation

Simply process each command in sequence:

```python
# Each "exclamation point" becomes "!"
# Result: "wow ! ! !" -> clean up spacing -> "wow!!!"
```

### Post-Processing Cleanup

```python
def clean_repeated_punctuation(text):
    """Remove spaces between repeated punctuation marks."""
    # "! ! !" -> "!!!"
    text = re.sub(r'([!?.])\s+(?=[!?.])', r'\1', text)
    return text
```

---

## 3. Punctuation at Start of Text

### The Problem

User says: "quote hello end quote"

First character is a quote - capitalization rules shouldn't apply to it.

### Solution

```python
def fix_capitalization(text):
    # Skip leading punctuation when capitalizing first character
    match = re.match(r'^([^\w]*)(.*)', text)
    if match:
        punctuation = match.group(1)
        rest = match.group(2)
        if rest and rest[0].islower():
            return punctuation + rest[0].upper() + rest[1:]
    return text
```

---

## 4. Compound Punctuation Commands

### The Problem

User says: "interrobang" or "question mark exclamation point"

### Solutions

```python
COMPOUND_PUNCTUATION = [
    ("question mark exclamation point", "?!"),
    ("exclamation point question mark", "!?"),
    ("interrobang", "?!"),  # If you want to support this
]

# Process compound commands before individual ones
```

---

## 5. Numbers Followed by Punctuation

### The Problem

User says: "one two three period"

Should this be "123." or "1 2 3."?

### Solution

Establish clear rules:

```python
# Sequential single digits become concatenated: "123"
# Compound numbers stay compound: "twenty three" -> "23"
# Punctuation follows the number

# "one two three period" -> "123."
# "twenty three period" -> "23."
```

---

## 6. Punctuation Command Substrings

### The Problem

"semicolon" contains "colon" - naive replacement could cause issues.

### Solution

Process longer commands first:

```python
PUNCTUATION_COMMANDS = [
    # Longer commands first
    ("semicolon", ";"),
    # Then shorter
    ("colon", ":"),
]

# Use word boundary matching
pattern = rf'\b{command}\b'
```

---

## 7. Mixed Case in Commands

### The Problem

Whisper might output "Period" or "PERIOD" instead of "period".

### Solution

Case-insensitive matching:

```python
pattern = re.compile(rf'\b{command}\b', re.IGNORECASE)
```

---

## 8. Commands Split Across Segments

### The Problem

With streaming/real-time transcription, a command might be split:

```
Segment 1: "hello new"
Segment 2: "line how are you"
```

### Solutions

#### Solution A: Buffer Partial Commands

```python
MULTI_WORD_COMMANDS = ["new line", "new paragraph", "question mark", ...]
COMMAND_PREFIXES = {"new", "question", "exclamation", "open", "close"}

def process_with_buffer(segment, buffer=""):
    combined = buffer + " " + segment
    combined = combined.strip()

    # Check if ends with a command prefix
    words = combined.split()
    if words and words[-1].lower() in COMMAND_PREFIXES:
        # Return processed text minus last word, buffer the last word
        return process(combined.rsplit(' ', 1)[0]), words[-1]
    else:
        return process(combined), ""
```

#### Solution B: Delayed Processing

Wait for natural pause or end-of-sentence before processing.

---

## 9. Ambiguous "Quote" Command

### The Problem

"quote" could be opening or closing.

### Solution

Track quote state:

```python
class QuoteTracker:
    def __init__(self):
        self.in_quote = False

    def process_quote(self):
        if self.in_quote:
            self.in_quote = False
            return '"'  # Closing quote
        else:
            self.in_quote = True
            return '"'  # Opening quote
```

Or use explicit commands:
- "open quote" / "begin quote" -> opening
- "close quote" / "end quote" -> closing
- "quote" -> toggle or always opening

---

## 10. Foreign Words and Names

### The Problem

Name "Colon" (Spanish) or word in context shouldn't be converted.

### Solution

This is fundamentally difficult to solve without context. Options:

1. **Accept false positives** - rare enough to not matter
2. **Require explicit commands** - "punctuation colon" instead of just "colon"
3. **Use NLP** - detect proper nouns and exclude them

### Pragmatic Approach

```python
# Most people don't say "colon" as a name frequently
# Accept occasional false positives
# Provide escape mechanism for when it matters
```

---

## 11. Acronyms and Abbreviations

### The Problem

"period" in "A period B period C period" (like "A.B.C.")

### Solution

This actually works correctly! Each "period" becomes a dot.

```python
# "A period B period C" -> "A. B. C."
# May want to clean up spaces: "A.B.C."
```

### Optional: Acronym Mode

```python
# "acronym A B C" -> "A.B.C."
# "spell A B C" -> "ABC"
```

---

## 12. Trailing Punctuation Commands

### The Problem

User says: "hello period" and pauses - should we wait for more or commit?

### Solution

For real-time systems, use timing:

```python
def process_with_timeout(segments, timeout_ms=500):
    """
    If last word is a punctuation command and
    there's been silence for timeout_ms, commit it.
    """
    pass
```

---

## 13. Whisper Already Converted Some Punctuation

### The Problem

Whisper inconsistently converts "comma" to "," sometimes.

### Solution

Handle both cases:

```python
def normalize_input(text):
    """Ensure consistent state before processing."""
    # Convert any existing punctuation back to words
    # (Optional - depends on desired behavior)

    # Or: just process commands, leave existing punctuation alone
    pass
```

Recommended: Leave existing punctuation alone, only process command words.

---

## Summary Table

| Edge Case | Recommended Solution |
|-----------|---------------------|
| Literal word needed | Escape command ("literal X") |
| Multiple punctuation | Process in sequence, clean spaces |
| Start of text | Skip punctuation when capitalizing |
| Compound punctuation | Process longer commands first |
| Numbers + punctuation | Clear precedence rules |
| Substring conflicts | Word boundary matching, length-order |
| Mixed case | Case-insensitive regex |
| Split across segments | Buffer partial commands |
| Ambiguous quote | State tracking or explicit commands |
| Foreign words/names | Accept rare false positives + escape |
| Acronyms | Works naturally |
| Trailing commands | Timeout-based commitment |
| Pre-converted punctuation | Process only command words |
