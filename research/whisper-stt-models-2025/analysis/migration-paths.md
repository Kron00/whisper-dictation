# Migration Paths: How to Switch Models/Frameworks

## Path 1: Staying with faster-whisper (Easy)

### Current -> Large-v3-Turbo

**Complexity:** Very Low
**Time:** 5 minutes

```python
# Before (your current setup)
from faster_whisper import WhisperModel

model = WhisperModel(
    "distil-whisper/distil-large-v3.5-ct2",
    device="cuda",
    compute_type="int8_float16"
)

# After (large-v3-turbo)
model = WhisperModel(
    "deepdml/faster-whisper-large-v3-turbo-ct2",
    device="cuda",
    compute_type="int8_float16"
)
```

**Changes:**
- Just change the model name
- Same API, same code
- Model downloads automatically on first use

**Expected Impact:**
- ~1.5x slower
- ~1% better WER
- ~2x more VRAM (still only 3GB)

---

### Current -> Large-v3 (Full)

**Complexity:** Very Low
**Time:** 5 minutes

```python
model = WhisperModel(
    "Systran/faster-whisper-large-v3",
    device="cuda",
    compute_type="int8_float16"
)
```

**Expected Impact:**
- ~2x slower
- ~1-2% better WER
- ~2.5x more VRAM (3.5-4GB)

---

## Path 2: Migrating to NeMo/Parakeet (Moderate)

### Step 1: Environment Setup

```bash
# Create new conda environment (recommended)
conda create -n nemo-dictation python=3.10 -y
conda activate nemo-dictation

# Install NeMo
pip install 'nemo_toolkit[asr]==2.4.0'

# Optional: For CUDA graphs optimization
pip install cuda-python>=12.3

# Verify
python -c "import nemo.collections.asr as nemo_asr; print('Ready')"
```

### Step 2: Basic Transcription

```python
import nemo.collections.asr as nemo_asr

# Load model (downloads ~1.2GB on first use)
model = nemo_asr.models.ASRModel.from_pretrained("nvidia/parakeet-tdt-0.6b-v2")

# Simple transcription
def transcribe_audio(audio_path: str) -> str:
    result = model.transcribe([audio_path])
    return result[0]

# Usage
text = transcribe_audio("recording.wav")
print(text)
```

### Step 3: With Word Timestamps

```python
def transcribe_with_timestamps(audio_path: str):
    result = model.transcribe([audio_path], return_hypotheses=True)

    text = result[0].text
    words = []

    if 'word' in result[0].timestep:
        for word_info in result[0].timestep['word']:
            words.append({
                'word': word_info['word'],
                'start': word_info['start_offset'],
                'end': word_info['end_offset']
            })

    return {'text': text, 'words': words}
```

### Step 4: Real-Time Dictation Integration

```python
import nemo.collections.asr as nemo_asr
import sounddevice as sd
import numpy as np
import queue
import threading

class ParakeetDictation:
    def __init__(self):
        self.model = nemo_asr.models.ASRModel.from_pretrained(
            "nvidia/parakeet-tdt-0.6b-v2"
        )
        self.audio_queue = queue.Queue()
        self.sample_rate = 16000

    def audio_callback(self, indata, frames, time, status):
        self.audio_queue.put(indata.copy())

    def process_audio(self, audio_data: np.ndarray) -> str:
        # Save to temp file (Parakeet requires file input)
        import tempfile
        import soundfile as sf

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            sf.write(f.name, audio_data, self.sample_rate)
            result = self.model.transcribe([f.name])
            return result[0]

    def start_dictation(self):
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=self.audio_callback
        ):
            print("Listening... (Press Ctrl+C to stop)")
            buffer = []
            while True:
                chunk = self.audio_queue.get()
                buffer.append(chunk)

                # Process every 3 seconds of audio
                if len(buffer) * len(chunk) > self.sample_rate * 3:
                    audio = np.concatenate(buffer)
                    text = self.process_audio(audio)
                    if text.strip():
                        print(text, end=" ", flush=True)
                    buffer = []

# Usage
dictation = ParakeetDictation()
dictation.start_dictation()
```

### Complexity Assessment

| Aspect | Effort |
|--------|--------|
| Environment setup | Low (10-15 min) |
| API learning | Low (similar concepts) |
| Code migration | Medium (different API) |
| Testing | Medium (verify accuracy) |
| **Total time** | **2-4 hours** |

---

## Path 3: Migrating to Kyutai/Moshi (Moderate)

### Step 1: Environment Setup

```bash
conda create -n moshi-dictation python=3.10 -y
conda activate moshi-dictation

pip install -U moshi
```

### Step 2: Basic Usage

```python
from moshi.models import stt

# Load model
model = stt.STT.from_pretrained("kyutai/stt-2.6b-en")
model = model.to("cuda")

# Transcribe file
result = model.transcribe("audio.mp3")
print(result["text"])
```

### Step 3: Streaming Transcription

```python
from moshi.models import stt
import sounddevice as sd
import numpy as np

class KyutaiDictation:
    def __init__(self):
        self.model = stt.STT.from_pretrained("kyutai/stt-2.6b-en")
        self.model = self.model.to("cuda")
        self.streamer = None

    def start_streaming(self):
        self.streamer = self.model.stream()

        def audio_callback(indata, frames, time, status):
            # Process incoming audio
            audio = indata[:, 0].astype(np.float32)
            text = self.streamer.process(audio)
            if text:
                print(text, end="", flush=True)

        with sd.InputStream(
            samplerate=16000,
            channels=1,
            callback=audio_callback,
            blocksize=1600  # 100ms chunks
        ):
            print("Streaming... (Press Ctrl+C to stop)")
            try:
                while True:
                    sd.sleep(100)
            except KeyboardInterrupt:
                print("\nStopped")

# Usage
dictation = KyutaiDictation()
dictation.start_streaming()
```

---

## Path 4: Parallel Testing Setup

Test multiple frameworks without commitment:

```bash
# Create separate environments
conda create -n faster-whisper-test python=3.10 -y
conda create -n nemo-test python=3.10 -y
conda create -n moshi-test python=3.10 -y

# Install in each
conda activate faster-whisper-test && pip install faster-whisper
conda activate nemo-test && pip install 'nemo_toolkit[asr]==2.4.0'
conda activate moshi-test && pip install moshi
```

### Benchmark Script

```python
import time
import sys

def benchmark_faster_whisper(audio_path):
    from faster_whisper import WhisperModel
    model = WhisperModel("distil-whisper/distil-large-v3.5-ct2",
                         device="cuda", compute_type="int8_float16")

    start = time.time()
    segments, _ = model.transcribe(audio_path)
    text = " ".join([s.text for s in segments])
    elapsed = time.time() - start

    return text, elapsed

def benchmark_parakeet(audio_path):
    import nemo.collections.asr as nemo_asr
    model = nemo_asr.models.ASRModel.from_pretrained("nvidia/parakeet-tdt-0.6b-v2")

    start = time.time()
    result = model.transcribe([audio_path])
    text = result[0]
    elapsed = time.time() - start

    return text, elapsed

def benchmark_kyutai(audio_path):
    from moshi.models import stt
    model = stt.STT.from_pretrained("kyutai/stt-2.6b-en")
    model = model.to("cuda")

    start = time.time()
    result = model.transcribe(audio_path)
    text = result["text"]
    elapsed = time.time() - start

    return text, elapsed

if __name__ == "__main__":
    audio_file = sys.argv[1]

    print("Testing faster-whisper...")
    fw_text, fw_time = benchmark_faster_whisper(audio_file)
    print(f"  Time: {fw_time:.2f}s")
    print(f"  Text: {fw_text[:100]}...")

    print("\nTesting Parakeet...")
    pk_text, pk_time = benchmark_parakeet(audio_file)
    print(f"  Time: {pk_time:.2f}s")
    print(f"  Text: {pk_text[:100]}...")

    print("\nTesting Kyutai...")
    ky_text, ky_time = benchmark_kyutai(audio_file)
    print(f"  Time: {ky_time:.2f}s")
    print(f"  Text: {ky_text[:100]}...")
```

---

## Migration Checklist

### Before Migration
- [ ] Backup current working configuration
- [ ] Prepare test audio files (various lengths, qualities)
- [ ] Document current performance metrics
- [ ] Note any custom code dependencies

### During Migration
- [ ] Create isolated test environment
- [ ] Install new framework
- [ ] Run basic transcription test
- [ ] Compare accuracy on test files
- [ ] Benchmark speed on test files
- [ ] Test with real-time audio input

### After Migration
- [ ] Verify VRAM usage acceptable
- [ ] Confirm latency meets requirements
- [ ] Test edge cases (accents, background noise)
- [ ] Update any dependent code
- [ ] Document new configuration

---

## Rollback Plan

If migration doesn't work out:

```bash
# Your original setup is always available
conda activate your-original-env
pip install faster-whisper

# Original code works unchanged
from faster_whisper import WhisperModel
model = WhisperModel("distil-whisper/distil-large-v3.5-ct2",
                     device="cuda", compute_type="int8_float16")
```

The original models remain on HuggingFace and faster-whisper is stable software.
