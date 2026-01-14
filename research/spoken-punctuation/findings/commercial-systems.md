# Commercial Dictation Systems: Punctuation Command Reference

## Dragon NaturallySpeaking

Dragon is considered the gold standard for voice dictation with the most comprehensive command set.

### Basic Punctuation Commands

| Say This | To Get This |
|----------|-------------|
| period / full stop | . |
| comma | , |
| question mark | ? |
| exclamation mark / exclamation point | ! |
| colon | : |
| semicolon | ; |
| apostrophe | ' |
| hyphen | - |
| dash | -- or -- |
| ellipsis | ... |

### Quote Commands

| Say This | To Get This |
|----------|-------------|
| open quote / begin quote | " |
| close quote / end quote | " |
| open single quote | ' |
| close single quote | ' |

### Bracket Commands

| Say This | To Get This |
|----------|-------------|
| open paren / open parenthesis | ( |
| close paren / close parenthesis | ) |
| open bracket | [ |
| close bracket | ] |
| open brace | { |
| close brace | } |

### Line and Paragraph

| Say This | Effect |
|----------|--------|
| new line | Press Enter once |
| new paragraph | Press Enter twice |
| tab key | Insert tab |

### Advanced Commands

- "Put quotes around that" - Wraps last phrase in quotes
- "Put parentheses around selection" - Wraps selected text
- "Scratch that" - Delete last utterance
- "Cap [word]" - Capitalize next word
- "All caps [word]" - Make next word uppercase

### Dragon Tips

- Pause before and after commands but not within them
- Natural Punctuation can auto-insert based on speech cadence
- Use "Show available commands window" to see all options

---

## macOS Dictation (Sonoma and later)

### Punctuation Commands

| Say This | To Get This |
|----------|-------------|
| period / point / dot / full stop | . |
| comma | , |
| question mark | ? |
| exclamation mark / exclamation point | ! |
| colon | : |
| semicolon | ; |
| apostrophe | ' |
| hyphen | - |
| dash | -- |
| ellipsis | ... |
| ampersand | & |
| asterisk | * |
| at sign | @ |
| backslash | \ |
| forward slash | / |
| percent sign | % |

### Quote Commands

| Say This | To Get This |
|----------|-------------|
| quote / open quote / begin quote | " |
| end quote / close quote | " |
| single quote / open single quote | ' |
| close single quote | ' |

### Bracket Commands

| Say This | To Get This |
|----------|-------------|
| open parenthesis | ( |
| close parenthesis | ) |
| open bracket | [ |
| close bracket | ] |
| open brace | { |
| close brace | } |
| less than sign | < |
| greater than sign | > |

### Line and Formatting

| Say This | Effect |
|----------|--------|
| new line | Line break (Return key once) |
| new paragraph | Paragraph break (Return key twice) |
| tab key | Insert tab character |
| no space on | Disable auto-spacing |
| no space off | Enable auto-spacing |

### Capitalization Commands

| Say This | Effect |
|----------|--------|
| caps on | Capitalize Each Word |
| caps off | return to normal |
| all caps | NEXT WORD UPPERCASE |
| all caps on | START ALL CAPS MODE |
| all caps off | end all caps mode |
| no caps | next word lowercase |
| no caps on | start all lowercase |
| no caps off | end all lowercase |

### Number Commands

| Say This | Effect |
|----------|--------|
| numeral [number] | Format as digit (e.g., "numeral five" -> "5") |
| roman numeral [number] | Format as Roman numeral |

### Special Characters

| Say This | To Get This |
|----------|-------------|
| degree sign | degree |
| copyright sign | (c) |
| registered sign | (R) |
| trademark sign | TM |
| dollar sign | $ |
| cent sign | c |
| pound sign | # |
| euro sign | EUR |
| yen sign | Y |
| plus sign | + |
| minus sign | - |
| equals sign | = |

### Emoji (macOS specific)

Say the emoji name followed by "emoji":
- "happy emoji" -> happy face
- "heart emoji" -> heart symbol
- "thumbs up emoji" -> thumbs up

### Auto-Punctuation Setting

Location: System Settings > Keyboard > Dictation > Auto-punctuation

When enabled, macOS automatically inserts commas, periods, and question marks based on speech patterns.

---

## Windows Voice Typing / Voice Access

### Enabling Voice Typing

- Keyboard shortcut: Win + H
- Or: Settings > Time & Language > Speech

### Punctuation Commands

| Say This | To Get This |
|----------|-------------|
| period / full stop | . |
| comma | , |
| question mark | ? |
| exclamation mark / exclamation point | ! |
| colon | : |
| semicolon | ; |
| apostrophe | ' |

### Quote and Bracket Commands

| Say This | To Get This |
|----------|-------------|
| open quote | " |
| close quote | " |
| open parenthesis | ( |
| close parenthesis | ) |
| open bracket | [ |
| close bracket | ] |

### Line and Formatting

| Say This | Effect |
|----------|--------|
| new line | Insert line break |
| new paragraph | Insert paragraph break |
| bold that | Bold last phrase |
| italics that | Italicize last phrase |
| underline that | Underline last phrase |

### Capitalization

| Say This | Effect |
|----------|--------|
| caps [word] | Capitalize next word |

### Escape Mechanism

To insert command words as literal text:
- Say "Type" or "Dictate" followed by the word
- Example: "Type period" inserts the word "period"

### Auto-Punctuation Setting

Location: Click gear icon in voice typing window > Automatic punctuation

When enabled, Windows detects punctuation from your tone and auto-inserts.

---

## Comparison Summary

| Feature | Dragon | macOS | Windows |
|---------|--------|-------|---------|
| Basic punctuation | Yes | Yes | Yes |
| Advanced quotes | Yes | Yes | Basic |
| Brackets/braces | Yes | Yes | Basic |
| "Wrap selection" | Yes | No | No |
| Emoji support | No | Yes | No |
| Numeral command | Limited | Yes | No |
| Auto-punctuation | Yes | Yes | Yes |
| Escape mechanism | No | Limited | Yes |
| Capitalization control | Extensive | Extensive | Basic |
| Undo ("scratch that") | Yes | Yes | Yes |

## Key Takeaway

All commercial systems use post-processing/command interpretation rather than expecting the speech recognition model to handle punctuation commands directly. This validates the approach of implementing custom post-processing for Whisper-based systems.
