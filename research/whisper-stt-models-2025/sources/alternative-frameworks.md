# Alternative Frameworks (Non-faster-whisper Options)

## Overview

While faster-whisper is excellent for Whisper-based models, several state-of-the-art ASR models require different frameworks. This document covers installation, usage, and considerations for each.

---

## 1. NVIDIA NeMo (Parakeet & Canary)

### Overview
NeMo is NVIDIA's toolkit for building and training conversational AI models. It provides the highest-performing open-source ASR models.

### Installation

```bash
# Create environment
conda create -n nemo-asr python=3.10 -y
conda activate nemo-asr

# Install NeMo ASR
pip install 'nemo_toolkit[asr]==2.4.0'

# For CUDA graphs optimization
pip install cuda-python>=12.3

# Verify installation
python -c "import nemo.collections.asr as nemo_asr; print('NeMo ASR ready')"
```

### Usage: Parakeet TDT 0.6B v2

```python
import nemo.collections.asr as nemo_asr

# Load model (downloads automatically)
model = nemo_asr.models.ASRModel.from_pretrained("nvidia/parakeet-tdt-0.6b-v2")

# Transcribe
transcription = model.transcribe(["audio.wav"])
print(transcription[0])

# Get word-level timestamps
transcription = model.transcribe(["audio.wav"], return_hypotheses=True)
for word_info in transcription[0].timestep['word']:
    print(f"{word_info['word']} [{word_info['start_offset']:.2f}s - {word_info['end_offset']:.2f}s]")
```

### Usage: Canary-Qwen-2.5B

```python
import nemo.collections.asr as nemo_asr

model = nemo_asr.models.ASRModel.from_pretrained("nvidia/canary-qwen-2.5b")
transcription = model.transcribe(["audio.wav"])
```

### Pros
- State-of-the-art accuracy and speed
- Native GPU optimization
- Word-level timestamps
- Punctuation and capitalization

### Cons
- Larger installation footprint
- Not compatible with faster-whisper ecosystem
- Requires NVIDIA GPU

### VRAM on RTX 3090
- Parakeet 0.6B: ~2-3GB (plenty of headroom)
- Canary 2.5B: ~5-6GB (fits easily)

---

## 2. Kyutai/Moshi STT

### Overview
Kyutai's STT models are optimized for real-time streaming with ultra-low latency. They use a decoder-only architecture based on the Mimi codec.

### Installation

```bash
# PyTorch version
pip install -U moshi

# For Apple Silicon
pip install -U moshi_mlx
```

### Usage: Streaming Transcription

```python
from moshi.models import stt

# Load model
model = stt.STT.from_pretrained("kyutai/stt-2.6b-en")
model = model.to("cuda")

# Transcribe file
result = model.transcribe("audio.mp3")
print(result["text"])

# Get word timestamps
for word in result["words"]:
    print(f"{word['word']} [{word['start']:.2f}s - {word['end']:.2f}s]")
```

### Usage: Real-Time Streaming

```python
from moshi.models import stt
import sounddevice as sd

model = stt.STT.from_pretrained("kyutai/stt-2.6b-en")
model = model.to("cuda")

# Stream from microphone
streamer = model.stream()
for chunk in sd.InputStream(samplerate=16000, channels=1):
    text = streamer.process(chunk)
    if text:
        print(text, end="", flush=True)
```

### Command-Line Usage

```bash
python -m moshi.run_inference --hf-repo kyutai/stt-2.6b-en audio.mp3
```

### Pros
- True streaming support (not chunked)
- Very low latency (0.5-2.5s initial)
- Good accuracy (6.4% WER)
- Word-level timestamps

### Cons
- Newer project (less community support)
- English-only for best model
- Requires ~6-8GB VRAM for 2.6B model

---

## 3. IBM Granite Speech

### Overview
IBM's Granite Speech models use a two-pass design with high accuracy on clean audio.

### Installation

```bash
pip install torch transformers accelerate
```

### Usage

```python
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
import torch

model_id = "ibm-granite/granite-speech-3.3-8b"

# Load model
processor = AutoProcessor.from_pretrained(model_id)
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    device_map="auto"
)

# Transcribe
audio = processor.feature_extractor(audio_array, sampling_rate=16000, return_tensors="pt")
generated_ids = model.generate(**audio)
transcription = processor.batch_decode(generated_ids, skip_special_tokens=True)
```

### Pros
- Very accurate on clean audio
- Multilingual support
- Standard HuggingFace interface

### Cons
- Slower than specialized ASR models
- 8B model requires ~16GB VRAM
- Two-pass design adds latency

---

## 4. Moonshine (Edge Devices)

### Overview
Moonshine is optimized for resource-constrained environments, running 5-15x faster than Whisper with comparable accuracy.

### Installation

```bash
pip install useful-moonshine
# Or from source
git clone https://github.com/moonshine-ai/moonshine.git
pip install -e moonshine/
```

### Usage

```python
from moonshine import transcribe

# Transcribe audio file
result = transcribe("audio.wav", model="moonshine/base")
print(result)
```

### Pros
- Extremely lightweight (<1GB VRAM)
- Fast inference
- Good for edge/embedded devices

### Cons
- Lower accuracy than larger models
- Limited features compared to full ASR systems

---

## 5. whisper.cpp (C++ Implementation)

### Overview
A C++ implementation of Whisper that can run on CPU or with CUDA support.

### Installation

```bash
git clone https://github.com/ggml-org/whisper.cpp.git
cd whisper.cpp

# CPU build
make

# CUDA build
make CUDA=1

# Download model
./models/download-ggml-model.sh large-v3
```

### Usage

```bash
# Transcribe
./main -m models/ggml-large-v3.bin -f audio.wav

# With GPU
./main -m models/ggml-large-v3.bin -f audio.wav --gpu
```

### Python Bindings

```bash
pip install whispercpp
```

```python
from whispercpp import Whisper

w = Whisper.from_pretrained("large-v3")
result = w.transcribe("audio.wav")
```

### Pros
- Runs on CPU efficiently
- Portable (single binary)
- CoreML support on Mac

### Cons
- Slower than faster-whisper on GPU
- Less Python integration
- Quality may vary from original

---

## 6. insanely-fast-whisper

### Overview
Maximum throughput implementation using FlashAttention-2 for high-end GPUs.

### Installation

```bash
pip install insanely-fast-whisper
# Requires FlashAttention-2
pip install flash-attn --no-build-isolation
```

### Usage

```bash
insanely-fast-whisper --file audio.mp3 --model-name openai/whisper-large-v3
```

```python
from insanely_fast_whisper import transcribe

result = transcribe("audio.mp3", model_name="openai/whisper-large-v3")
```

### Pros
- 12-36x faster than OpenAI Whisper
- 3-4x faster than faster-whisper
- Good for batch processing

### Cons
- Requires high-end GPU (A100 optimal)
- FlashAttention-2 compilation needed
- Overkill for real-time dictation

---

## Comparison Summary

| Framework | Best Model | Speed | Accuracy | Setup Complexity | RTX 3090 Fit |
|-----------|------------|-------|----------|------------------|--------------|
| faster-whisper | distil-large-v3.5 | Good | Good | Easy | Yes |
| NeMo | Parakeet TDT 0.6B | Excellent | Excellent | Medium | Yes |
| Moshi | stt-2.6b-en | Good | Excellent | Easy | Yes |
| Transformers | Granite 8B | Slow | Excellent | Easy | Yes |
| whisper.cpp | large-v3 | Moderate | Good | Medium | Yes |
| insanely-fast | large-v3 | Excellent | Good | Hard | Yes |
| Moonshine | base | Excellent | Moderate | Easy | Yes |

---

## Recommendation for Your Use Case

**For real-time dictation on RTX 3090:**

1. **Stay with faster-whisper** if current setup works well
   - Mature, stable, well-documented
   - Your distil-large-v3.5-ct2 is excellent

2. **Try NeMo + Parakeet TDT 0.6B v2** for significant speed improvement
   - 50x faster than Whisper
   - Better accuracy (6.05% vs ~7.5% WER)
   - Worth the framework switch

3. **Try Kyutai STT** for true streaming
   - Best initial latency
   - Native streaming (not chunked)
   - Newer but promising
