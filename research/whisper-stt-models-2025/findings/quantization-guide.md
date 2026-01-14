# Quantization Options Guide for RTX 3090

## Overview

Quantization reduces model precision to improve speed and reduce memory usage. The RTX 3090 (Ampere architecture, SM 8.6) supports various quantization methods via its 3rd-generation Tensor Cores.

---

## RTX 3090 Supported Precision Types

| Type | Description | Tensor Core Support |
|------|-------------|---------------------|
| FP32 | 32-bit floating point | Yes |
| FP16 | 16-bit floating point | Yes |
| BF16 | Brain Float 16 | Yes |
| TF32 | TensorFloat 32 | Yes |
| INT8 | 8-bit integer | Yes |
| INT4 | 4-bit integer | Yes |

---

## faster-whisper Compute Types

### Available Options

```python
from faster_whisper import WhisperModel

# Option 1: Full FP16 (highest quality)
model = WhisperModel("distil-whisper/distil-large-v3.5-ct2",
                     device="cuda",
                     compute_type="float16")

# Option 2: INT8 with FP16 fallback (RECOMMENDED for GPU)
model = WhisperModel("distil-whisper/distil-large-v3.5-ct2",
                     device="cuda",
                     compute_type="int8_float16")

# Option 3: INT8 with FP32 fallback (typically for CPU)
model = WhisperModel("distil-whisper/distil-large-v3.5-ct2",
                     device="cpu",
                     compute_type="int8")
```

### Comparison

| Compute Type | Non-Quantized Layers | Memory | Speed | Quality | Best For |
|--------------|---------------------|--------|-------|---------|----------|
| float16 | FP16 | Highest | Fast | Best | Maximum accuracy |
| int8_float16 | FP16 | ~40% less | Faster | Near-identical | **GPU inference (recommended)** |
| int8 | FP32 | Lowest | Varies | Slight degradation | CPU inference |

---

## Benchmarks: int8_float16 vs float16

### GPU Memory Usage (faster-whisper)

| Model | float16 | int8_float16 | Savings |
|-------|---------|--------------|---------|
| large-v3 | 5-6GB | 3.5-4GB | ~35% |
| large-v3-turbo | 4.5GB | 3GB | ~33% |
| distil-large-v3.5 | 2.4GB | 1.5GB | ~38% |

### Processing Speed (13-min audio)

| Model | float16 | int8_float16 | Speedup |
|-------|---------|--------------|---------|
| large-v3-turbo | 19.16s | 19.59s | ~same |
| distil-large-v3 | 26.13s | 22.54s | ~15% faster |

### Word Error Rate

| Model | float16 WER | int8_float16 WER | Difference |
|-------|-------------|------------------|------------|
| large-v3-turbo | 1.919 | 1.919 | None |
| distil-large-v3 | 2.392 | 2.392 | None |

**Conclusion:** int8_float16 provides memory savings with negligible quality loss.

---

## Recommendation for RTX 3090

### Your Current Setup: OPTIMAL

```python
model = WhisperModel(
    "distil-whisper/distil-large-v3.5-ct2",
    device="cuda",
    compute_type="int8_float16"
)
```

**Why this is optimal:**

1. **Memory Efficiency:** ~1.5GB VRAM leaves 22.5GB free for other tasks
2. **Speed:** int8 quantization on Tensor Cores is highly optimized
3. **Quality:** No measurable WER degradation
4. **Headroom:** Can process longer audio or batch multiple files

### When to Use float16 Instead

- If you need absolute maximum accuracy (edge cases)
- If VRAM is not a concern and you want simplicity
- If benchmarking for quality comparisons

### When to Use int8 (FP32 fallback)

- CPU-only inference
- Systems without FP16 Tensor Core support
- Debugging purposes

---

## CTranslate2 Quantization During Conversion

When converting models with `ct2-transformers-converter`:

```bash
# FP16 quantization (recommended for GPU)
ct2-transformers-converter --model openai/whisper-large-v3-turbo \
    --output_dir whisper-turbo-ct2 \
    --quantization float16

# INT8 quantization (smaller file size)
ct2-transformers-converter --model openai/whisper-large-v3-turbo \
    --output_dir whisper-turbo-ct2-int8 \
    --quantization int8

# INT16 quantization (balance)
ct2-transformers-converter --model openai/whisper-large-v3-turbo \
    --output_dir whisper-turbo-ct2-int16 \
    --quantization int16
```

**Note:** The model weights are saved in the specified format, but you can change the compute type at runtime using the `compute_type` parameter.

---

## Advanced: BF16 on RTX 3090

The RTX 3090 supports BF16 via Tensor Cores. However, CTranslate2/faster-whisper does not currently expose BF16 as a compute type. This is primarily relevant for:

- Custom NeMo models
- PyTorch native inference
- Training/fine-tuning

---

## Performance Tips for RTX 3090

### Maximize Throughput

```python
from faster_whisper import WhisperModel, BatchedInferencePipeline

model = WhisperModel(
    "distil-whisper/distil-large-v3.5-ct2",
    device="cuda",
    compute_type="int8_float16",
    num_workers=4  # Parallel processing
)

# Use batched inference for multiple files
batched_model = BatchedInferencePipeline(model=model)
```

### Minimize Latency (Real-Time Dictation)

```python
model = WhisperModel(
    "distil-whisper/distil-large-v3.5-ct2",
    device="cuda",
    compute_type="int8_float16"
)

# Use beam_size=1 for fastest single-pass decoding
segments, _ = model.transcribe(
    audio,
    beam_size=1,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=500)
)
```

### CUDA Configuration

```bash
# Ensure CUDA 12 + cuDNN 9 for latest ctranslate2
# Or use ctranslate2==3.24.0 for CUDA 11

# Set visible device
export CUDA_VISIBLE_DEVICES=0
```

---

## Summary: Quantization Decision Tree

```
Need maximum accuracy AND have VRAM to spare?
  |-- Yes --> Use float16
  |-- No --> Use int8_float16

Running on CPU only?
  |-- Yes --> Use int8
  |-- No --> Use int8_float16

Converting model for distribution?
  |-- Save as float16, let users choose compute_type at runtime
```
