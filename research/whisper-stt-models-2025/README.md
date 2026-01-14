# Whisper Speech-to-Text Models Research: Best Options for RTX 3090 (Late 2025)

**Research Date:** December 6, 2025
**Target Hardware:** NVIDIA RTX 3090 (24GB VRAM)
**Use Case:** Real-time dictation with fast transcription
**Current Setup:** faster-whisper with distil-whisper/distil-large-v3.5-ct2 (int8_float16)

---

## Executive Summary

### Top 5 Key Findings

1. **Your current model (distil-large-v3.5-ct2) is excellent** - It remains one of the best choices for real-time English dictation with faster-whisper. It's ~1.5x faster than Whisper-large-v3-turbo while maintaining near-identical accuracy.

2. **NVIDIA Parakeet TDT 0.6B v2/v3 offers superior speed** - With RTFx of 3386 (vs ~216 for Whisper Turbo), it's ~50x faster than Whisper models. However, it requires NeMo framework and is NOT compatible with faster-whisper/CTranslate2.

3. **For maximum accuracy within faster-whisper**, Whisper large-v3-turbo-ct2 slightly edges out distil-large-v3.5 (~1% lower WER) but is 1.5x slower.

4. **int8_float16 quantization is optimal for RTX 3090** - It provides the best speed/accuracy tradeoff with minimal quality loss and ~40% memory savings vs float16.

5. **Non-Whisper alternatives (Parakeet, Canary, Kyutai) require different frameworks** but offer state-of-the-art accuracy and speed for those willing to switch from faster-whisper.

---

## Folder Structure

```
research-whisper-stt-models-2025/
|-- README.md                          # This file - overview and recommendations
|-- findings/
|   |-- main-findings.md               # Core research synthesis
|   |-- model-comparison-table.md      # Detailed comparison matrix
|   |-- quantization-guide.md          # Quantization options analysis
|-- sources/
|   |-- huggingface-models.md          # HuggingFace model links and details
|   |-- benchmarks.md                  # Speed and accuracy benchmarks
|   |-- alternative-frameworks.md      # Non-faster-whisper options
|-- analysis/
|   |-- recommendations.md             # Final ranked recommendations
|   |-- migration-paths.md             # How to switch models/frameworks
```

---

## Quick Recommendations

### If staying with faster-whisper (recommended for your use case):

| Rank | Model | Why |
|------|-------|-----|
| 1 | **distil-whisper/distil-large-v3.5-ct2** | Your current model - best speed/accuracy for English dictation |
| 2 | **deepdml/faster-whisper-large-v3-turbo-ct2** | ~1% better WER, 1.5x slower than distil |
| 3 | **Systran/faster-whisper-large-v3** | Most accurate, but 2x slower than distil |

### If willing to switch frameworks (for maximum performance):

| Rank | Model | Framework | Why |
|------|-------|-----------|-----|
| 1 | **NVIDIA Parakeet TDT 0.6B v2** | NeMo | 50x faster than Whisper, 6.05% WER |
| 2 | **NVIDIA Canary-Qwen-2.5B** | NeMo | Best accuracy (5.63% WER), 418 RTFx |
| 3 | **Kyutai STT 2.6B** | Moshi/PyTorch | Real-time streaming, 6.4% WER |

---

## Limitations & Caveats

- Benchmarks vary by dataset, audio quality, and hardware configuration
- RTFx/speed measurements can differ significantly between implementations
- Non-Whisper models require different installation procedures and dependencies
- Fine-tuned models for specific domains may outperform general models
- Some newer models (late 2025) may have limited community support

---

## Suggestions for Further Research

1. Test Parakeet TDT 0.6B v2 on your RTX 3090 to compare real-world latency
2. Benchmark RealtimeSTT library with your preferred model
3. Explore Kyutai STT for streaming applications if latency is critical
4. Monitor Hugging Face Open ASR Leaderboard for new model releases
5. Consider fine-tuning distil-large-v3.5 on dictation-specific data if needed
