# Main Research Findings: Whisper STT Models (Late 2025)

## 1. Latest Whisper Models from OpenAI

### Whisper Large-v3-Turbo (Latest Official Release)
- **Release:** October 2024 (still current as of late 2025)
- **Parameters:** 809M (reduced from 1550M in large-v3)
- **Architecture:** 32 encoder layers, 4 decoder layers (reduced from 32)
- **Speed:** 8x faster than large-v3, RTFx ~216
- **VRAM:** ~6GB (vs ~10GB for large-v3)
- **WER:** Within 1-2% of large-v3
- **CTranslate2:** Available as `deepdml/faster-whisper-large-v3-turbo-ct2`

### OpenAI gpt-4o-transcribe (Cloud Only)
- Fine-tuned specifically for transcription
- Sets the "frontier model baseline" for accuracy
- Not available for local deployment

---

## 2. Distil-Whisper Variants

### distil-whisper/distil-large-v3.5 (March 2025 - LATEST)
- **Parameters:** 0.8B
- **Training Data:** 98k hours (4x more than predecessors)
- **Architecture:** 32 encoder layers, 2 decoder layers
- **Speed:** ~2x faster than Whisper-large-v3, ~1.5x faster than large-v3-turbo
- **Optimal Chunk Length:** 25 seconds
- **Languages:** Multilingual (inherited from large-v3)
- **Available Formats:**
  - CTranslate2: `distil-whisper/distil-large-v3.5-ct2` (your current model)
  - ONNX: `distil-whisper/distil-large-v3.5-ONNX`
  - GGML: `distil-whisper/distil-large-v3.5-ggml`
  - OpenAI format: `distil-whisper/distil-large-v3.5-openai`

### distil-whisper/distil-large-v3 (Previous Version)
- Slightly faster but less accurate than v3.5
- CTranslate2: `distil-whisper/distil-large-v3-ct2`

### Community Fine-Tunes
- **jacktol/whisper-medium.en-fine-tuned-for-ATC-faster-whisper** - Air Traffic Control optimized
- Various language-specific fine-tunes available

---

## 3. Alternative Architectures (Non-Whisper)

### NVIDIA Parakeet TDT Family

**Parakeet TDT 0.6B v2** (English-only)
- **Parameters:** 600M
- **Architecture:** FastConformer encoder + Token Duration Transducer (TDT) decoder
- **Speed:** RTFx 3386 (transcribes 60 minutes in 1 second)
- **WER:** 6.05% (best-in-class among open models)
- **Max Audio:** 24 minutes
- **Features:** Word-level timestamps, punctuation, capitalization
- **Framework:** NVIDIA NeMo (NOT compatible with faster-whisper)
- **VRAM:** ~2-3GB estimated for inference

**Parakeet TDT 0.6B v3** (Multilingual)
- Extends v2 with 25 European languages
- Same speed characteristics

**Parakeet TDT 1.1B**
- **Speed:** RTFx ~2000+, 64% faster than Parakeet RNNT 1.1B
- **WER:** First model to achieve <7.0% average WER on Open ASR leaderboard
- Better accuracy but requires more VRAM

**Parakeet CTC 1.1B**
- **Speed:** RTFx 2793.75 (fastest on leaderboard)
- **WER:** 6.68%
- Best for maximum throughput

### NVIDIA Canary Family

**Canary-Qwen-2.5B**
- **Parameters:** 2.5B
- **Architecture:** FastConformer encoder + Qwen LLM decoder
- **Speed:** RTFx 418
- **WER:** 5.63% (TOPS Hugging Face Open ASR Leaderboard)
- **Languages:** English only
- **Framework:** NVIDIA NeMo
- **VRAM:** ~5GB FP16 estimated

**Canary 1B v2**
- **Languages:** 25 EU languages
- **Speed:** Comparable to models 3x larger, 10x faster inference
- **Framework:** NVIDIA NeMo

**Canary 1B Flash**
- **Architecture:** 32 encoder, 4 decoder layers
- **Speed:** >1000 RTFx
- Optimized for inference speed

### Kyutai/Moshi STT

**kyutai/stt-2.6b-en** (English-only)
- **Parameters:** 2.6B
- **Architecture:** Decoder-only, based on Mimi codec
- **Latency:** 2.5 second initial delay, then real-time
- **WER:** 6.4%
- **Features:** Streaming inference, word-level timestamps
- **Framework:** PyTorch or MLX
- **License:** CC-BY 4.0

**kyutai/stt-1b-en_fr** (English + French)
- **Parameters:** ~1B
- **Latency:** 0.5 second delay
- Built-in semantic VAD

### IBM Granite Speech

**ibm-granite/granite-speech-3.3-8b**
- **Parameters:** 8B
- **Architecture:** Two-pass design (ASR + LLM)
- **WER:** 8.18% (best on clean audio in some benchmarks)
- **Languages:** EN, FR, DE, ES, PT + translations
- **Framework:** PyTorch/Transformers
- **VRAM:** ~16GB FP16

**ibm-granite/granite-speech-3.3-2b**
- Smaller variant for resource-constrained environments

### Moonshine (Edge Devices)

**UsefulSensors/moonshine**
- **Size:** Tiny (~27M) and Base variants
- **Speed:** 5-15x faster than equivalent Whisper models
- **Memory:** Can run in <8MB RAM
- **WER:** 12.81% (Tiny), comparable to Whisper Tiny
- **Best For:** Edge devices, embedded systems
- **2025 Update:** Multilingual variants (Arabic, Chinese, Japanese, Korean, Ukrainian, Vietnamese)

---

## 4. Speed vs Accuracy Trade-offs

### Benchmark Summary (Open ASR Leaderboard Late 2025)

| Model | WER (%) | RTFx | Notes |
|-------|---------|------|-------|
| NVIDIA Canary-Qwen-2.5B | 5.63 | 418 | Best accuracy |
| NVIDIA Parakeet TDT 0.6B v2 | 6.05 | 3386 | Best speed/accuracy |
| Kyutai STT 2.6B | 6.4 | ~300 | Best streaming |
| Whisper Large-v3 | 6.43 | 68.56 | Baseline |
| Parakeet CTC 1.1B | 6.68 | 2793.75 | Maximum speed |
| IBM Granite Speech 8B | 8.18 | ~50 | Clean audio champion |
| Distil-Whisper Large-v3.5 | ~7-8 | ~140 | Best faster-whisper |
| Moonshine Tiny | 12.81 | ~500+ | Edge devices |

### Real-Time Factor Explained
- RTFx = Real-Time Factor multiplier
- RTFx 100 = Transcribes 100 seconds of audio in 1 second
- RTFx 216 (Whisper Turbo) = Still "plenty of speed for real-time"
- RTFx 3386 (Parakeet TDT 0.6B) = 60 minutes in 1 second

---

## 5. CTranslate2/faster-whisper Compatible Models

### Official Systran Models
- `Systran/faster-whisper-tiny`
- `Systran/faster-whisper-base`
- `Systran/faster-whisper-small`
- `Systran/faster-whisper-medium`
- `Systran/faster-whisper-large-v3`
- `Systran/faster-distil-whisper-large-v2`

### Official Distil-Whisper CTranslate2
- `distil-whisper/distil-large-v3.5-ct2` (RECOMMENDED)
- `distil-whisper/distil-large-v3-ct2`

### Community CTranslate2 Conversions
- `deepdml/faster-whisper-large-v3-turbo-ct2`
- `deepdml/faster-distil-whisper-large-v3.5`
- `Purfview/faster-distil-whisper-large-v3.5`

### Converting Custom Models
```bash
ct2-transformers-converter --model openai/whisper-large-v3-turbo \
    --output_dir whisper-large-v3-turbo-ct2 \
    --copy_files tokenizer.json preprocessor_config.json \
    --quantization float16
```

**Requirements:**
- transformers >= 4.23.0
- ctranslate2 (latest requires CUDA 12 + cuDNN 9)
- For CUDA 11: downgrade to ctranslate2==3.24.0

---

## 6. Quantization Options for RTX 3090

### faster-whisper Compute Types

| Type | Description | VRAM | Speed | Quality |
|------|-------------|------|-------|---------|
| float16 | Full FP16 on GPU | Highest | Fast | Best |
| int8_float16 | INT8 + FP16 for non-quantized layers | ~40% less | Faster | Near-identical |
| int8 | INT8 + FP32 (typically CPU) | Lowest | Varies | Slightly degraded |

### Recommended for RTX 3090 (24GB VRAM)
**int8_float16** - Your current choice is optimal:
- Provides ~40% memory savings vs float16
- Minimal accuracy loss
- Faster inference than pure float16
- Plenty of headroom on 24GB for batch processing

### VRAM Usage Estimates (faster-whisper)

| Model | float16 | int8_float16 |
|-------|---------|--------------|
| large-v3-turbo | ~4.5GB | ~3GB |
| large-v3 | ~5-6GB | ~3.5-4GB |
| distil-large-v3.5 | ~2.4GB | ~1.5GB |

---

## 7. English-Only Optimized Models

### Built-in English Models
- `whisper-tiny.en`, `whisper-base.en`, `whisper-small.en`, `whisper-medium.en`
- Generally perform better on English than multilingual equivalents
- Fewer parameters, faster inference

### Best English-Only Options

1. **NVIDIA Parakeet TDT 0.6B v2** - State-of-the-art English ASR
2. **NVIDIA Canary-Qwen-2.5B** - Highest accuracy English model
3. **Kyutai STT 2.6B** - Best streaming English
4. **distil-whisper/distil-large-v3.5** - Best faster-whisper compatible

### Note on Distil-Whisper
Distil-Whisper models are multilingual but trained with emphasis on English. Performance on non-English languages may be degraded compared to full Whisper models.

---

## 8. Dictation-Specific Considerations

### Why Dictation Differs from Transcription
- Real-time latency requirements (<300ms ideal)
- Voice Activity Detection (VAD) integration critical
- Punctuation and capitalization important
- Speaker typically near microphone (clean audio)
- Short utterances vs long-form audio

### Best Models for Dictation

**If using faster-whisper:**
1. distil-large-v3.5-ct2 with int8_float16 (your current setup)
2. Use Silero VAD for voice detection
3. Consider RealtimeSTT library for end-to-end solution

**If maximum speed needed:**
1. NVIDIA Parakeet TDT 0.6B v2 (requires NeMo)
2. Kyutai STT (native streaming support)

### Recommended Libraries for Real-Time Dictation
- **RealtimeSTT** - Built on faster-whisper, includes VAD
- **WhisperLive** - Collabora's near-live implementation
- **faster-whisper** with Silero VAD - DIY approach

### Configuration Tips
- Use VAD to segment audio at natural pauses
- Process short chunks (2-10 seconds) for low latency
- `condition_on_previous_text=False` for streaming (prevents error accumulation)
- Beam size 1 for fastest inference (beam size 5 for accuracy)
