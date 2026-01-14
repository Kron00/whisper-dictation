"""
Number Word Processor for Voice Dictation Systems

This module converts spoken number words to digits, handling both
compound numbers ("twenty three" -> 23) and sequential digits
("one two three" -> "123").

Requires: pip install word2number

Usage:
    from number_processor import NumberProcessor

    processor = NumberProcessor()
    result = processor.process("I have twenty three apples")
    # Result: "I have 23 apples"

Author: Research compilation
Date: 2025-12-06
"""

import re
from typing import Optional
from dataclasses import dataclass, field


# Number word definitions
ONES = {
    'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4,
    'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9,
    'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13,
    'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 'seventeen': 17,
    'eighteen': 18, 'nineteen': 19
}

TENS = {
    'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50,
    'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90
}

SCALES = {
    'hundred': 100,
    'thousand': 1000,
    'million': 1000000,
    'billion': 1000000000,
    'trillion': 1000000000000
}

ALL_NUMBER_WORDS = set(ONES.keys()) | set(TENS.keys()) | set(SCALES.keys()) | {'and', 'a'}


@dataclass
class NumberConfig:
    """Configuration for number processing."""

    # Convert compound numbers like "twenty three" to "23"
    convert_compound: bool = True

    # Convert sequential single digits like "one two three" to "123"
    convert_sequential: bool = True

    # Convert ordinals like "first" "second" to "1st" "2nd"
    convert_ordinals: bool = False

    # Maximum sequential digits to concatenate
    max_sequential_digits: int = 10

    # Words that indicate number mode (like macOS "numeral" command)
    number_mode_triggers: list = field(default_factory=lambda: [
        "numeral",
        "number",
    ])


class NumberProcessor:
    """
    Converts spoken number words to digits.

    Handles two types of number expressions:
    1. Compound numbers: "twenty three" -> "23"
    2. Sequential digits: "one two three" -> "123"

    The distinction is made by context:
    - If words form a valid compound number, they're summed
    - If single digits appear in sequence without compounds, they're concatenated
    """

    def __init__(self, config: Optional[NumberConfig] = None):
        """Initialize with optional configuration."""
        self.config = config or NumberConfig()

    def process(self, text: str) -> str:
        """
        Process text to convert number words to digits.

        Args:
            text: Input text with number words

        Returns:
            Text with number words converted to digits
        """
        if not text:
            return text

        # Handle explicit number mode triggers
        text = self._handle_number_mode(text)

        # Process the rest of the text
        words = text.split()
        result = []
        i = 0

        while i < len(words):
            # Check if current word starts a number sequence
            word_clean = self._clean_word(words[i])

            if word_clean.lower() in ALL_NUMBER_WORDS:
                # Found a number word - collect the full sequence
                number_sequence, end_idx = self._collect_number_sequence(words, i)

                if number_sequence:
                    # Determine type and convert
                    converted = self._convert_number_sequence(number_sequence)

                    # Preserve any trailing punctuation from the last word
                    trailing = self._get_trailing_punctuation(words[end_idx - 1])
                    result.append(converted + trailing)

                    i = end_idx
                else:
                    result.append(words[i])
                    i += 1
            else:
                result.append(words[i])
                i += 1

        return " ".join(result)

    def _clean_word(self, word: str) -> str:
        """Remove punctuation from word for comparison."""
        return re.sub(r'[^\w]', '', word.lower())

    def _get_trailing_punctuation(self, word: str) -> str:
        """Extract trailing punctuation from a word."""
        match = re.search(r'[^\w]+$', word)
        return match.group(0) if match else ""

    def _collect_number_sequence(self, words: list, start: int) -> tuple:
        """
        Collect consecutive number words.

        Returns:
            Tuple of (list of number words, end index)
        """
        sequence = []
        i = start

        while i < len(words):
            word_clean = self._clean_word(words[i])

            # Skip "and" in middle of numbers ("one hundred and twenty")
            if word_clean == 'and' and sequence:
                i += 1
                continue

            # Skip "a" as "a hundred" = "one hundred"
            if word_clean == 'a' and i + 1 < len(words):
                next_clean = self._clean_word(words[i + 1])
                if next_clean in SCALES:
                    sequence.append('one')
                    i += 1
                    continue

            if word_clean in ALL_NUMBER_WORDS and word_clean not in ['and', 'a']:
                sequence.append(word_clean)
                i += 1
            else:
                break

        return sequence, i

    def _convert_number_sequence(self, sequence: list) -> str:
        """
        Convert a sequence of number words to digits.

        Determines if sequence is compound or sequential and converts accordingly.
        """
        if not sequence:
            return ""

        # Check if this is a sequence of single digits
        if self._is_sequential_digits(sequence):
            return self._convert_sequential_digits(sequence)
        else:
            return self._convert_compound_number(sequence)

    def _is_sequential_digits(self, sequence: list) -> bool:
        """
        Determine if sequence should be treated as sequential digits.

        Sequential: "one two three" (all single digits, no tens/scales)
        Compound: "twenty three" or "one hundred"
        """
        if not self.config.convert_sequential:
            return False

        # If any tens or scales, it's compound
        for word in sequence:
            if word in TENS or word in SCALES:
                return False

        # If all are single digits (0-9), treat as sequential
        single_digits = {'zero', 'one', 'two', 'three', 'four',
                        'five', 'six', 'seven', 'eight', 'nine'}

        return all(word in single_digits for word in sequence)

    def _convert_sequential_digits(self, sequence: list) -> str:
        """Convert sequence of single digit words to concatenated string."""
        digits = []
        for word in sequence[:self.config.max_sequential_digits]:
            if word in ONES:
                digits.append(str(ONES[word]))
        return "".join(digits)

    def _convert_compound_number(self, sequence: list) -> str:
        """
        Convert compound number words to a single number.

        Uses a stack-based algorithm to handle:
        - "twenty three" -> 23
        - "one hundred twenty three" -> 123
        - "two thousand three hundred forty five" -> 2345
        """
        if not self.config.convert_compound:
            return " ".join(sequence)

        try:
            return str(self._text_to_int(sequence))
        except (ValueError, KeyError):
            # If conversion fails, return original words
            return " ".join(sequence)

    def _text_to_int(self, words: list) -> int:
        """
        Convert list of number words to integer.

        Algorithm handles compound numbers with scales.
        """
        if not words:
            raise ValueError("Empty word list")

        current = 0
        result = 0

        for word in words:
            if word in ONES:
                current += ONES[word]
            elif word in TENS:
                current += TENS[word]
            elif word in SCALES:
                scale = SCALES[word]
                if current == 0:
                    current = 1
                if scale >= 1000:
                    # For thousand and above, add to result and reset
                    result += current * scale
                    current = 0
                else:
                    # For hundred, just multiply current
                    current *= scale
            else:
                raise ValueError(f"Unknown number word: {word}")

        return result + current

    def _handle_number_mode(self, text: str) -> str:
        """
        Handle explicit number mode triggers.

        "numeral five five five" -> "555"
        """
        for trigger in self.config.number_mode_triggers:
            pattern = rf'\b{trigger}\s+([\w\s]+?)(?=[.!?,;:]|\s*$)'

            def convert_match(match):
                number_text = match.group(1).strip()
                # Force sequential mode for triggered numbers
                words = [self._clean_word(w) for w in number_text.split()
                        if self._clean_word(w) in ONES]
                if words:
                    return self._convert_sequential_digits(words)
                return match.group(0)

            text = re.sub(pattern, convert_match, text, flags=re.IGNORECASE)

        return text


def process_numbers(text: str) -> str:
    """
    Convenience function to process number words.

    Args:
        text: Input text with number words

    Returns:
        Text with number words converted to digits
    """
    processor = NumberProcessor()
    return processor.process(text)


# Example usage and tests
if __name__ == "__main__":
    processor = NumberProcessor()

    test_cases = [
        # Compound numbers
        ("I have twenty three apples", "I have 23 apples"),
        ("one hundred twenty three", "123"),
        ("two thousand three hundred forty five", "2345"),
        ("a hundred dollars", "100 dollars"),

        # Sequential digits
        ("my zip code is one two three four five", "my zip code is 12345"),
        ("call me at five five five one two three four",
         "call me at 5551234"),

        # Mixed
        ("I have twenty three at one two three main street",
         "I have 23 at 123 main street"),

        # Ordinals (not converted by default)
        ("this is the first test", "this is the first test"),

        # With punctuation
        ("twenty three.", "23."),
        ("one, two, three", "1, 2, 3"),

        # Number mode trigger
        ("numeral five five five", "555"),
    ]

    print("Number Processor Tests")
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
