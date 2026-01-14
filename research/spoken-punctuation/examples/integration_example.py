"""
Complete Integration Example: Whisper + Spoken Punctuation Processing

This module demonstrates how to integrate the punctuation processor with
faster-whisper for a complete voice dictation system that handles:
- Speech-to-text via faster-whisper
- Spoken punctuation commands ("period" -> ".")
- Number word conversion ("twenty three" -> "23")
- Filler word removal
- Automatic capitalization

Requirements:
    pip install faster-whisper word2number

Usage:
    python integration_example.py audio.wav

Author: Research compilation
Date: 2025-12-06
"""

import sys
import time
from pathlib import Path
from typing import Optional, Iterator

# Import our processors
from punctuation_processor import PunctuationProcessor, PunctuationConfig
from number_processor import NumberProcessor, NumberConfig


class VoiceDictationPipeline:
    """
    Complete voice dictation pipeline with punctuation command support.

    This class combines:
    1. faster-whisper for speech-to-text
    2. Spoken punctuation command processing
    3. Number word conversion
    4. Filler word removal
    5. Capitalization correction
    """

    def __init__(
        self,
        model_size: str = "base",
        device: str = "auto",
        compute_type: str = "auto",
        language: Optional[str] = None,
    ):
        """
        Initialize the dictation pipeline.

        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            device: Device to use (cpu, cuda, auto)
            compute_type: Compute type (int8, float16, float32, auto)
            language: Language code (en, es, etc.) or None for auto-detect
        """
        self.model_size = model_size
        self.device = device
        self.compute_type = compute_type
        self.language = language

        # Initialize processors
        self._init_processors()

        # Lazy load whisper model
        self._whisper_model = None

    def _init_processors(self):
        """Initialize text processors."""
        # Punctuation processor config
        punct_config = PunctuationConfig(
            convert_punctuation=True,
            convert_numbers=False,  # We'll use our own number processor
            remove_fillers=True,
            fix_capitalization=True,
            clean_whitespace=True,
        )
        self.punct_processor = PunctuationProcessor(punct_config)

        # Number processor config
        number_config = NumberConfig(
            convert_compound=True,
            convert_sequential=True,
            convert_ordinals=False,
        )
        self.number_processor = NumberProcessor(number_config)

    @property
    def whisper_model(self):
        """Lazy load Whisper model."""
        if self._whisper_model is None:
            try:
                from faster_whisper import WhisperModel
            except ImportError:
                raise ImportError(
                    "faster-whisper is required. Install with: pip install faster-whisper"
                )

            print(f"Loading Whisper model: {self.model_size}...")
            self._whisper_model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=self.compute_type,
            )
            print("Model loaded.")

        return self._whisper_model

    def transcribe(
        self,
        audio_path: str,
        beam_size: int = 5,
        vad_filter: bool = True,
    ) -> str:
        """
        Transcribe audio file with punctuation command processing.

        Args:
            audio_path: Path to audio file
            beam_size: Beam size for decoding
            vad_filter: Whether to use VAD filtering

        Returns:
            Processed transcription text
        """
        # Verify file exists
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Transcribe with Whisper
        print(f"Transcribing: {audio_path}")
        start_time = time.time()

        segments, info = self.whisper_model.transcribe(
            audio_path,
            beam_size=beam_size,
            vad_filter=vad_filter,
            language=self.language,
        )

        # Collect raw text from segments
        raw_text = ""
        for segment in segments:
            raw_text += segment.text

        transcribe_time = time.time() - start_time
        print(f"Transcription complete in {transcribe_time:.2f}s")
        print(f"Detected language: {info.language} (probability: {info.language_probability:.2f})")

        # Post-process
        processed_text = self.process_text(raw_text)

        return processed_text

    def transcribe_realtime(
        self,
        audio_stream: Iterator[bytes],
        sample_rate: int = 16000,
    ) -> Iterator[str]:
        """
        Process audio stream in real-time.

        Args:
            audio_stream: Iterator yielding audio chunks
            sample_rate: Audio sample rate

        Yields:
            Processed text chunks
        """
        # This is a simplified example - real implementation would need:
        # - Audio buffering
        # - VAD for sentence detection
        # - Handling of partial transcriptions

        buffer = b""

        for chunk in audio_stream:
            buffer += chunk

            # Process when we have enough audio (e.g., 2 seconds)
            if len(buffer) >= sample_rate * 2 * 2:  # 2 seconds of 16-bit audio
                # Save buffer to temp file (faster-whisper needs file)
                import tempfile
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                    # Write WAV header and data
                    self._write_wav(f, buffer, sample_rate)
                    temp_path = f.name

                # Transcribe chunk
                try:
                    result = self.transcribe(temp_path)
                    if result.strip():
                        yield result
                finally:
                    Path(temp_path).unlink()

                buffer = b""

    def process_text(self, text: str) -> str:
        """
        Apply all post-processing to raw transcription text.

        Processing order:
        1. Punctuation commands
        2. Number conversion
        3. (Filler removal and capitalization handled by punct_processor)

        Args:
            text: Raw transcription text

        Returns:
            Processed text
        """
        # Step 1: Punctuation commands (includes filler removal and capitalization)
        text = self.punct_processor.process(text)

        # Step 2: Number conversion (optional, can be slow for long texts)
        # Uncomment if you want number conversion:
        # text = self.number_processor.process(text)

        return text

    def _write_wav(self, file, data: bytes, sample_rate: int):
        """Write WAV file header and data."""
        import struct

        # WAV header
        file.write(b'RIFF')
        file.write(struct.pack('<I', 36 + len(data)))
        file.write(b'WAVE')
        file.write(b'fmt ')
        file.write(struct.pack('<I', 16))  # Subchunk1Size
        file.write(struct.pack('<H', 1))   # AudioFormat (PCM)
        file.write(struct.pack('<H', 1))   # NumChannels
        file.write(struct.pack('<I', sample_rate))  # SampleRate
        file.write(struct.pack('<I', sample_rate * 2))  # ByteRate
        file.write(struct.pack('<H', 2))   # BlockAlign
        file.write(struct.pack('<H', 16))  # BitsPerSample
        file.write(b'data')
        file.write(struct.pack('<I', len(data)))
        file.write(data)


def demo_without_whisper():
    """Demonstrate text processing without Whisper."""
    print("=" * 60)
    print("Demo: Text Processing Only (no Whisper)")
    print("=" * 60)

    # Create processors
    punct_processor = PunctuationProcessor()
    number_processor = NumberProcessor()

    # Example inputs (simulating Whisper output)
    examples = [
        # Basic punctuation
        "hello period how are you question mark",

        # Multiple punctuation types
        "dear john comma i hope this letter finds you well period",

        # Quotes and parentheses
        "he said open quote hello world close quote",

        # Line breaks
        "first paragraph new paragraph second paragraph",

        # Numbers
        "my phone number is five five five one two three four",

        # Complex example with fillers
        "um so basically the meeting is at um two thirty period i think we should uh discuss the budget comma which is um twenty three thousand dollars period",

        # Edge case: literal word
        "the literal period of history was quite interesting period",
    ]

    for i, text in enumerate(examples, 1):
        print(f"\nExample {i}:")
        print(f"  Input:  {text}")

        # Process punctuation
        result = punct_processor.process(text)
        print(f"  Output: {result}")

        # Optionally process numbers too
        result_with_numbers = number_processor.process(result)
        if result_with_numbers != result:
            print(f"  +Numbers: {result_with_numbers}")


def demo_with_whisper(audio_path: str):
    """Demonstrate full pipeline with Whisper."""
    print("=" * 60)
    print("Demo: Full Pipeline with Whisper")
    print("=" * 60)

    pipeline = VoiceDictationPipeline(
        model_size="base",
        device="auto",
        compute_type="auto",
    )

    result = pipeline.transcribe(audio_path)

    print(f"\nFinal result:")
    print("-" * 40)
    print(result)
    print("-" * 40)


def interactive_mode():
    """Interactive text processing mode."""
    print("=" * 60)
    print("Interactive Mode")
    print("Type text with spoken punctuation commands.")
    print("Commands: period, comma, question mark, new line, etc.")
    print("Press Ctrl+C to exit.")
    print("=" * 60)

    punct_processor = PunctuationProcessor()
    number_processor = NumberProcessor()

    try:
        while True:
            text = input("\nInput: ")
            if text.strip():
                result = punct_processor.process(text)
                result = number_processor.process(result)
                print(f"Output: {result}")
    except KeyboardInterrupt:
        print("\n\nGoodbye!")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Voice dictation with spoken punctuation support"
    )
    parser.add_argument(
        "audio",
        nargs="?",
        help="Path to audio file to transcribe"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run text processing demo (no Whisper)"
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Interactive text processing mode"
    )
    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
        help="Whisper model size"
    )

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.demo:
        demo_without_whisper()
    elif args.audio:
        pipeline = VoiceDictationPipeline(model_size=args.model)
        result = pipeline.transcribe(args.audio)
        print("\n" + "=" * 60)
        print("RESULT:")
        print("=" * 60)
        print(result)
    else:
        # Default: run demo
        demo_without_whisper()
        print("\n" + "=" * 60)
        print("To transcribe audio: python integration_example.py <audio_file>")
        print("For interactive mode: python integration_example.py --interactive")


if __name__ == "__main__":
    main()
