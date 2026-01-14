# Comprehensive Model Comparison Table

## Models Compatible with faster-whisper/CTranslate2

| Model | HuggingFace ID | Params | WER (approx) | RTFx | VRAM (FP16) | VRAM (int8) | English-Only | Recommended For |
|-------|----------------|--------|--------------|------|-------------|-------------|--------------|-----------------|
| Distil-Large-v3.5 | `distil-whisper/distil-large-v3.5-ct2` | 0.8B | ~7-8% | ~140 | ~2.4GB | ~1.5GB | No (but optimized) | **Best overall for dictation** |
| Large-v3-Turbo | `deepdml/faster-whisper-large-v3-turbo-ct2` | 0.8B | ~6.5% | ~90 | ~4.5GB | ~3GB | No | Best accuracy in faster-whisper |
| Large-v3 | `Systran/faster-whisper-large-v3` | 1.55B | ~6.4% | ~68 | ~5-6GB | ~3.5GB | No | Maximum accuracy (slower) |
| Distil-Large-v3 | `distil-whisper/distil-large-v3-ct2` | 0.8B | ~8% | ~120 | ~2.4GB | ~1.5GB | No | Legacy, use v3.5 instead |
| Medium.en | `Systran/faster-whisper-medium.en` | 0.77B | ~9% | ~150 | ~2GB | ~1.2GB | Yes | Budget English-only |
| Small.en | `Systran/faster-whisper-small.en` | 0.24B | ~11% | ~300 | ~0.5GB | ~0.3GB | Yes | Low VRAM/CPU |

---

## Models Requiring NeMo Framework (NOT faster-whisper compatible)

| Model | HuggingFace ID | Params | WER | RTFx | VRAM (est.) | English-Only | Recommended For |
|-------|----------------|--------|-----|------|-------------|--------------|-----------------|
| Parakeet TDT 0.6B v2 | `nvidia/parakeet-tdt-0.6b-v2` | 0.6B | 6.05% | 3386 | ~2-3GB | Yes | **Best speed + accuracy** |
| Parakeet TDT 0.6B v3 | `nvidia/parakeet-tdt-0.6b-v3` | 0.6B | ~6% | 3386 | ~2-3GB | No (25 EU langs) | Multilingual speed |
| Parakeet TDT 1.1B | `nvidia/parakeet-tdt-1.1b` | 1.1B | <7% | ~2000 | ~4-5GB | Yes | Better accuracy than 0.6B |
| Parakeet CTC 1.1B | `nvidia/parakeet-ctc-1.1b` | 1.1B | 6.68% | 2793 | ~4-5GB | Yes | Maximum throughput |
| Canary-Qwen-2.5B | `nvidia/canary-qwen-2.5b` | 2.5B | 5.63% | 418 | ~5-6GB | Yes | **Best accuracy overall** |
| Canary 1B v2 | `nvidia/canary-1b-v2` | 1B | ~7% | ~1000 | ~3-4GB | No (25 langs) | Multilingual accuracy |
| Canary 1B Flash | `nvidia/canary-1b-flash` | 1B | ~7.5% | >1000 | ~3-4GB | No | Fast multilingual |

---

## Models Requiring Other Frameworks

| Model | Framework | Params | WER | RTFx | VRAM | English-Only | Recommended For |
|-------|-----------|--------|-----|------|------|--------------|-----------------|
| Kyutai STT 2.6B | PyTorch/MLX | 2.6B | 6.4% | ~300 | ~6-8GB | Yes | Real-time streaming |
| Kyutai STT 1B | PyTorch/MLX | 1B | ~7% | ~500 | ~3-4GB | No (EN+FR) | Low-latency streaming |
| Granite Speech 8B | Transformers | 8B | 8.18% | ~50 | ~16GB | No | Clean audio, enterprise |
| Granite Speech 2B | Transformers | 2B | ~10% | ~100 | ~4-5GB | No | Resource-constrained |
| Moonshine Tiny | Custom | 27M | 12.81% | ~500+ | <1GB | Yes | Edge/embedded devices |

---

## Detailed faster-whisper Benchmarks

### Test Conditions
- Hardware: RTX 3070 Ti 8GB / RTX 4070 Laptop GPU (varies by source)
- Audio: 13 minutes test file
- CUDA 12.4

### Results (13-minute audio file)

| Model | Compute Type | Time (s) | WER | GPU Memory |
|-------|--------------|----------|-----|------------|
| faster-large-v3-turbo | fp16 | 19.16 | 1.919 | ~4.5GB |
| faster-large-v3-turbo | int8 | 19.59 | 1.919 | ~3GB |
| faster-distil-large-v3 | fp16 | 26.13 | 2.392 | ~2.4GB |
| faster-distil-large-v3 | int8 | 22.54 | 2.392 | ~1.5GB |
| faster-large-v3 | fp16 | ~45 | ~1.8 | ~5GB |

**Note:** distil-large-v3.5 should perform similarly to distil-large-v3 in speed with slightly better accuracy.

---

## Speed Ranking (Fastest to Slowest)

### For Real-Time Dictation (Lower is Better for Latency)

1. **Parakeet TDT 0.6B v2** - RTFx 3386 (transcribes 60 min in 1 sec)
2. **Parakeet CTC 1.1B** - RTFx 2793
3. **Parakeet TDT 1.1B** - RTFx ~2000
4. **Canary 1B Flash** - RTFx >1000
5. **Kyutai STT 1B** - 0.5s initial latency
6. **Moonshine** - 5-15x faster than Whisper
7. **Canary-Qwen-2.5B** - RTFx 418
8. **Distil-Large-v3.5** - RTFx ~140
9. **Large-v3-Turbo** - RTFx ~90-216
10. **Whisper Large-v3** - RTFx ~68

---

## Accuracy Ranking (Best WER to Worst)

### On Open ASR Leaderboard Benchmarks

1. **Canary-Qwen-2.5B** - 5.63% WER
2. **Parakeet TDT 0.6B v2** - 6.05% WER
3. **Kyutai STT 2.6B** - 6.4% WER
4. **Whisper Large-v3** - 6.43% WER
5. **Whisper Large-v3-Turbo** - ~6.5% WER
6. **Parakeet CTC 1.1B** - 6.68% WER
7. **Distil-Large-v3.5** - ~7-8% WER
8. **Granite Speech 8B** - 8.18% WER (best on clean audio)
9. **Medium.en** - ~9% WER
10. **Moonshine Tiny** - 12.81% WER

---

## VRAM Requirements Summary

### For RTX 3090 (24GB) - All Models Will Fit Comfortably

| VRAM Range | Models |
|------------|--------|
| <2GB | Moonshine, Small.en, distil (int8) |
| 2-4GB | Parakeet 0.6B, Medium, distil (fp16), Turbo (int8) |
| 4-6GB | Turbo (fp16), Large-v3, Canary-Qwen, Parakeet 1.1B |
| 6-10GB | Kyutai 2.6B, Large-v3 (fp16) |
| 10-16GB | Granite Speech 8B |

**Your RTX 3090 can run ANY of these models without VRAM constraints.**

---

## Framework Compatibility Matrix

| Model Family | faster-whisper | NeMo | Transformers | whisper.cpp | MLX |
|--------------|----------------|------|--------------|-------------|-----|
| Whisper (OpenAI) | Yes | Via Riva | Yes | Yes | Yes |
| Distil-Whisper | Yes | No | Yes | Yes (GGML) | Yes |
| Parakeet | No | Yes | No | No | No |
| Canary | No | Yes | No | No | No |
| Kyutai STT | No | No | Yes | No | Yes |
| Granite Speech | No | No | Yes | No | No |
| Moonshine | No | No | Yes | No | Yes |
