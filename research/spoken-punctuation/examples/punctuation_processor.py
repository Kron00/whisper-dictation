"""
Spoken Punctuation Processor for Voice Dictation Systems

This module converts spoken punctuation commands (like "period", "comma",
"new line") into actual punctuation marks and formatting. Designed for
post-processing Whisper/faster-whisper transcriptions.

Usage:
    from punctuation_processor import PunctuationProcessor

    processor = PunctuationProcessor()
    result = processor.process("hello comma how are you question mark")
    # Result: "Hello, how are you?"

Author: Research compilation
Date: 2025-12-06
"""

import re
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class PunctuationConfig:
    """Configuration for the punctuation processor."""

    # Feature toggles
    convert_punctuation: bool = True
    convert_numbers: bool = False  # Requires word2number library
    remove_fillers: bool = True
    fix_capitalization: bool = True
    clean_whitespace: bool = True

    # Escape prefix for literal words
    escape_prefixes: list = field(default_factory=lambda: [
        "literal",
        "the word",
        "spell out",
    ])

    # Filler words to remove
    filler_words: list = field(default_factory=lambda: [
        "um", "uh", "uhm", "umm", "er", "err", "ah", "ahh",
        "like", "you know", "i mean", "sort of", "kind of",
        "basically", "actually", "literally",
    ])

    # Custom punctuation commands (added to defaults)
    custom_commands: list = field(default_factory=list)


# Default punctuation command mappings
# Order matters: longer/more specific commands first to avoid partial matches
PUNCTUATION_COMMANDS = [
    # Multi-word commands (process first)
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
    ("left quote", '"'),
    ("right quote", '"'),
    ("single quote", "'"),
    ("new paragraph", "\n\n"),
    ("new line", "\n"),
    ("newline", "\n"),

    # Single-word commands (process after multi-word)
    ("period", "."),
    ("dot", "."),
    ("fullstop", "."),
    ("comma", ","),
    ("colon", ":"),
    ("semicolon", ";"),
    ("hyphen", "-"),
    ("dash", "-"),
    ("ellipsis", "..."),
    ("apostrophe", "'"),
    ("quote", '"'),

    # Extended symbols (optional - can be disabled)
    ("ampersand", "&"),
    ("asterisk", "*"),
    ("at sign", "@"),
    ("percent", "%"),
    ("percent sign", "%"),
    ("dollar sign", "$"),
    ("hash", "#"),
    ("hashtag", "#"),
    ("pound sign", "#"),
    ("plus sign", "+"),
    ("minus sign", "-"),
    ("equals", "="),
    ("equals sign", "="),
    ("underscore", "_"),
    ("backslash", "\\"),
    ("forward slash", "/"),
    ("slash", "/"),
]


class PunctuationProcessor:
    """
    Processes text to convert spoken punctuation commands to actual punctuation.

    Features:
    - Converts "period" to "."
    - Converts "comma" to ","
    - Converts "new line" to actual newline
    - Supports escape mechanism ("literal period" -> "period")
    - Optional filler word removal
    - Optional capitalization correction
    - Optional number word conversion

    Example:
        processor = PunctuationProcessor()
        text = "hello comma world period how are you question mark"
        result = processor.process(text)
        # Result: "Hello, world. How are you?"
    """

    def __init__(self, config: Optional[PunctuationConfig] = None):
        """
        Initialize the processor with optional configuration.

        Args:
            config: PunctuationConfig instance, or None for defaults
        """
        self.config = config or PunctuationConfig()

        # Build command list (custom commands first, then defaults)
        self.commands = list(self.config.custom_commands) + PUNCTUATION_COMMANDS

        # Pre-compile regex patterns for efficiency
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile regex patterns for better performance."""
        # Escape patterns
        self.escape_patterns = []
        for prefix in self.config.escape_prefixes:
            # Match: escape_prefix + space + word
            pattern = re.compile(
                rf'\b{re.escape(prefix)}\s+(\w+)',
                re.IGNORECASE
            )
            self.escape_patterns.append(pattern)

        # Punctuation command patterns
        self.command_patterns = []
        for command, symbol in self.commands:
            # Match command as whole word (with word boundaries)
            pattern = re.compile(
                rf'\b{re.escape(command)}\b',
                re.IGNORECASE
            )
            self.command_patterns.append((pattern, symbol))

        # Filler word patterns
        self.filler_patterns = []
        for filler in self.config.filler_words:
            pattern = re.compile(
                rf'\b{re.escape(filler)}\b',
                re.IGNORECASE
            )
            self.filler_patterns.append(pattern)

    def process(self, text: str) -> str:
        """
        Process text through the complete pipeline.

        Args:
            text: Raw transcription text

        Returns:
            Processed text with punctuation commands converted

        Pipeline order:
            1. Handle escape commands
            2. Convert punctuation commands
            3. Convert numbers (optional)
            4. Remove filler words
            5. Fix capitalization
            6. Clean whitespace
            7. Restore escaped literals
        """
        if not text or not isinstance(text, str):
            return ""

        # Step 1: Handle escape commands (protect literal words)
        text, literals = self._handle_escapes(text)

        # Step 2: Convert punctuation commands
        if self.config.convert_punctuation:
            text = self._convert_punctuation(text)

        # Step 3: Convert number words (optional)
        if self.config.convert_numbers:
            text = self._convert_numbers(text)

        # Step 4: Remove filler words
        if self.config.remove_fillers:
            text = self._remove_fillers(text)

        # Step 5: Fix capitalization
        if self.config.fix_capitalization:
            text = self._fix_capitalization(text)

        # Step 6: Clean whitespace
        if self.config.clean_whitespace:
            text = self._clean_whitespace(text)

        # Step 7: Restore escaped literals
        text = self._restore_literals(text, literals)

        return text

    def _handle_escapes(self, text: str) -> tuple[str, dict]:
        """
        Handle escape commands to protect literal words.

        "literal period" -> "__LITERAL_0__" (stored: "period")

        Returns:
            Tuple of (processed text, dict of literals)
        """
        literals = {}
        counter = 0

        for pattern in self.escape_patterns:
            def replace_literal(match, counter=counter, literals=literals):
                word = match.group(1)
                placeholder = f"__LITERAL_{counter}__"
                literals[placeholder] = word
                return placeholder

            # Find all matches and replace
            matches = list(pattern.finditer(text))
            for match in reversed(matches):  # Reverse to maintain positions
                word = match.group(1)
                placeholder = f"__LITERAL_{counter}__"
                literals[placeholder] = word
                text = text[:match.start()] + placeholder + text[match.end():]
                counter += 1

        return text, literals

    def _restore_literals(self, text: str, literals: dict) -> str:
        """Restore escaped literal words."""
        for placeholder, word in literals.items():
            text = text.replace(placeholder, word)
        return text

    def _convert_punctuation(self, text: str) -> str:
        """Convert spoken punctuation commands to symbols."""
        for pattern, symbol in self.command_patterns:
            text = self._replace_with_spacing(text, pattern, symbol)
        return text

    def _replace_with_spacing(self, text: str, pattern: re.Pattern, symbol: str) -> str:
        """
        Replace pattern with symbol, handling spacing appropriately.

        Rules:
        - Sentence-ending punctuation (.!?): no space before, space after
        - Commas/colons/semicolons: no space before, space after
        - Opening brackets/quotes: space before, no space after
        - Closing brackets/quotes: no space before, space after
        - Newlines: replace surrounding spaces
        """
        def get_replacement(match):
            # Determine appropriate spacing based on symbol type
            if symbol in ".!?,:;":
                # No space before, ensure space after (will be cleaned up later)
                return symbol + " "
            elif symbol in "([{":
                # Space before, no space after
                return " " + symbol
            elif symbol in ")]}":
                # No space before, space after
                return symbol + " "
            elif symbol == '"':
                # This is tricky - could be opening or closing
                # For simplicity, just replace with symbol
                return symbol
            elif symbol == "'":
                # Apostrophe - no spaces
                return symbol
            elif symbol in "\n":
                # Newline - remove surrounding spaces
                return symbol
            else:
                # Default: just the symbol
                return symbol

        text = pattern.sub(get_replacement, text)
        return text

    def _convert_numbers(self, text: str) -> str:
        """
        Convert number words to digits.

        Requires: pip install word2number

        Examples:
            "twenty three" -> "23"
            "one two three" -> "123"
        """
        try:
            from word2number import w2n
        except ImportError:
            # word2number not installed, skip conversion
            return text

        # This is a simplified implementation
        # A full implementation would need to:
        # 1. Identify number word sequences
        # 2. Determine if they're compound (twenty three) or sequential (one two three)
        # 3. Convert appropriately

        # For now, just handle simple cases
        number_words = [
            "zero", "one", "two", "three", "four", "five",
            "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen", "twenty",
            "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
            "hundred", "thousand", "million", "billion"
        ]

        # Find sequences of number words and convert them
        words = text.split()
        result = []
        number_buffer = []

        for word in words:
            word_lower = word.lower().strip('.,!?;:')
            if word_lower in number_words:
                number_buffer.append(word_lower)
            else:
                if number_buffer:
                    # Try to convert the number sequence
                    try:
                        number_str = " ".join(number_buffer)
                        number = w2n.word_to_num(number_str)
                        result.append(str(number))
                    except ValueError:
                        # If conversion fails, keep original words
                        result.extend(number_buffer)
                    number_buffer = []
                result.append(word)

        # Don't forget remaining buffer
        if number_buffer:
            try:
                number_str = " ".join(number_buffer)
                number = w2n.word_to_num(number_str)
                result.append(str(number))
            except ValueError:
                result.extend(number_buffer)

        return " ".join(result)

    def _remove_fillers(self, text: str) -> str:
        """Remove filler words and disfluencies."""
        for pattern in self.filler_patterns:
            text = pattern.sub("", text)
        return text

    def _fix_capitalization(self, text: str) -> str:
        """
        Fix capitalization after sentence-ending punctuation.

        Rules:
        - Capitalize after . ! ?
        - Capitalize after paragraph breaks
        - Capitalize first character of text
        """
        # Capitalize after sentence-ending punctuation
        text = re.sub(
            r'([.!?])\s+([a-z])',
            lambda m: m.group(1) + " " + m.group(2).upper(),
            text
        )

        # Capitalize after paragraph breaks
        text = re.sub(
            r'(\n\n)([a-z])',
            lambda m: m.group(1) + m.group(2).upper(),
            text
        )

        # Capitalize after single newline (optional - depends on desired behavior)
        text = re.sub(
            r'(\n)([a-z])',
            lambda m: m.group(1) + m.group(2).upper(),
            text
        )

        # Capitalize first character (skip leading punctuation/whitespace)
        match = re.match(r'^(\s*[^\w\s]*\s*)([a-z])', text)
        if match:
            text = match.group(1) + match.group(2).upper() + text[match.end():]

        return text

    def _clean_whitespace(self, text: str) -> str:
        """Clean up whitespace issues."""
        # Remove multiple spaces
        text = re.sub(r' +', ' ', text)

        # Remove space before punctuation
        text = re.sub(r'\s+([.!?,;:])', r'\1', text)

        # Remove space after opening brackets/quotes
        text = re.sub(r'([\[({"])\s+', r'\1', text)

        # Remove space before closing brackets/quotes
        text = re.sub(r'\s+([\])}"])', r'\1', text)

        # Ensure space after closing punctuation (but not at end)
        text = re.sub(r'([.!?,;:])([^\s.!?,;:\n])', r'\1 \2', text)

        # Clean up multiple newlines (max 2)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Trim leading/trailing whitespace
        text = text.strip()

        return text


# Convenience function for simple usage
def process_punctuation(text: str) -> str:
    """
    Simple convenience function to process punctuation commands.

    Args:
        text: Raw transcription text

    Returns:
        Processed text with punctuation commands converted

    Example:
        result = process_punctuation("hello comma world period")
        # Result: "Hello, world."
    """
    processor = PunctuationProcessor()
    return processor.process(text)


# Example usage and tests
if __name__ == "__main__":
    # Create processor
    processor = PunctuationProcessor()

    # Test cases
    test_cases = [
        # Basic punctuation
        ("hello period", "Hello."),
        ("how are you question mark", "How are you?"),
        ("wow exclamation point", "Wow!"),
        ("one comma two comma three", "One, two, three."),

        # Multiple punctuation
        ("hello period how are you question mark", "Hello. How are you?"),

        # Quotes and brackets
        ("he said open quote hello close quote", 'He said "hello".'),
        ("open paren see above close paren", "(See above)."),

        # Line breaks
        ("first line new line second line", "First line.\nSecond line."),
        ("first paragraph new paragraph second paragraph",
         "First paragraph.\n\nSecond paragraph."),

        # Complex example
        ("um hello comma how are you question mark i am fine comma thanks exclamation point",
         "Hello, how are you? I am fine, thanks!"),

        # Escape mechanism
        ("the literal period of history was important period",
         "The period of history was important."),
    ]

    print("Punctuation Processor Tests")
    print("=" * 60)

    for input_text, expected in test_cases:
        result = processor.process(input_text)
        status = "PASS" if result == expected else "FAIL"
        print(f"\n{status}: {input_text[:40]}...")
        print(f"  Expected: {expected}")
        print(f"  Got:      {result}")

    print("\n" + "=" * 60)
    print("Interactive mode - enter text to process (Ctrl+C to exit):")

    try:
        while True:
            user_input = input("\n> ")
            if user_input.strip():
                result = processor.process(user_input)
                print(f"Result: {result}")
    except KeyboardInterrupt:
        print("\nGoodbye!")
