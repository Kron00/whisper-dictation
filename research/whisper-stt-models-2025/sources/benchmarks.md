# Speed and Accuracy Benchmarks

## Sources

Primary benchmark sources used in this research:
- [Hugging Face Open ASR Leaderboard](https://huggingface.co/spaces/hf-audio/open_asr_leaderboard)
- [Northflank STT Benchmarks 2025](https://northflank.com/blog/best-open-source-speech-to-text-stt-model-in-2025-benchmarks)
- [Modal Blog: Open Source STT](https://modal.com/blog/open-source-stt)
- [NVIDIA Developer Blog](https://developer.nvidia.com/blog/nvidia-speech-ai-models-deliver-industry-leading-accuracy-and-performance/)
- [faster-whisper GitHub Issues](https://github.com/SYSTRAN/faster-whisper/issues/1030)

---

## Open ASR Leaderboard Results (November 2025)

### English Transcription - Average WER

| Rank | Model | WER (%) | RTFx | Organization |
|------|-------|---------|------|--------------|
| 1 | Canary-Qwen-2.5B | 5.63 | 418 | NVIDIA |
| 2 | Parakeet TDT 0.6B v2 | 6.05 | 3386 | NVIDIA |
| 3 | Canary 1B Flash | ~6.2 | >1000 | NVIDIA |
| 4 | Canary 1B | ~6.3 | ~800 | NVIDIA |
| 5 | Whisper Large-v3 | 6.43 | 68.56 | OpenAI |
| 6 | Whisper Large-v3-Turbo | ~6.5 | 216 | OpenAI |
| 7 | Kyutai STT 2.6B | 6.4 | ~300 | Kyutai |
| 8 | Parakeet CTC 1.1B | 6.68 | 2793.75 | NVIDIA |
| 9 | Distil-Whisper Large-v3.5 | ~7.5 | ~140 | Hugging Face |
| 10 | Granite Speech 8B | 8.18 | ~50 | IBM |

### Key Observations
- Conformer encoders + LLM decoders achieve best WER but are slower
- CTC and TDT decoders deliver much better RTFx (throughput)
- NVIDIA models dominate both accuracy and speed rankings

---

## faster-whisper Specific Benchmarks

### Test Setup
- Hardware: NVIDIA RTX 3070 Ti 8GB
- CUDA: 12.4
- Audio: 13 minutes
- Benchmark: LibriSpeech clean validation split

### Results

| Model | Compute Type | Time (s) | WER | GPU Memory |
|-------|--------------|----------|-----|------------|
| faster-large-v3-turbo | fp16 | 19.155 | 1.919 | ~4.5GB |
| faster-large-v3-turbo | int8 | 19.591 | 1.919 | ~3GB |
| faster-distil-large-v3 | fp16 | 26.126 | 2.392 | ~2.4GB |
| faster-distil-large-v3 | int8 | 22.537 | 2.392 | ~1.5GB |
| faster-large-v3 | fp16 | ~45 | ~1.8 | ~5GB |

### Analysis
- Large-v3-turbo is ~35% faster than distil-large-v3 with better WER
- int8 quantization provides ~15% speedup for distil models with no WER change
- int8 vs fp16 shows negligible speed difference for turbo model

---

## Real-Time Factor (RTFx) Explained

RTFx = (Audio Duration) / (Processing Time)

| RTFx | Meaning | Example |
|------|---------|---------|
| 1 | Real-time | 60s audio in 60s |
| 10 | 10x faster | 60s audio in 6s |
| 100 | 100x faster | 60s audio in 0.6s |
| 216 | Whisper Turbo | 60s audio in 0.28s |
| 3386 | Parakeet TDT | 60min audio in 1s |

**For real-time dictation:** RTFx > 10 is sufficient; RTFx > 100 enables batch processing.

---

## Latency Benchmarks (Real-Time Applications)

### Initial Response Latency

| Model | Initial Latency | Streaming Support |
|-------|-----------------|-------------------|
| Kyutai STT 1B | 0.5s | Yes |
| Kyutai STT 2.6B | 2.5s | Yes |
| Whisper (any) | Chunk-dependent | Pseudo-streaming |
| Parakeet TDT | <100ms | Via NeMo |
| Deepgram Nova-3 | <300ms | Yes (API) |
| ElevenLabs Scribe | <150ms | Yes (API) |

### Chunk Processing Latency (faster-whisper)

For 10-second audio chunks:
- distil-large-v3.5 (int8_float16): ~0.5-1s on RTX 3090
- large-v3-turbo (int8_float16): ~0.3-0.5s on RTX 3090

---

## Accuracy by Audio Type

### Clean Speech (LibriSpeech test-clean)

| Model | WER (%) |
|-------|---------|
| Granite Speech 8B | 8.18 |
| Whisper Large-v3 | ~4.5 |
| Parakeet TDT 0.6B | ~5 |
| Distil-Large-v3.5 | ~5.5 |

### Noisy/Real-World Audio

| Model | WER (%) | Notes |
|-------|---------|-------|
| Canary-Qwen-2.5B | 5.63 | Best overall |
| Parakeet TDT | 6.05 | Robust |
| Whisper Large-v3 | 6.43 | Good robustness |
| Distil-Large-v3.5 | 7-8 | "Noise robust" training |

### Long-Form Audio (Podcasts, Lectures)

| Model | Performance | Notes |
|-------|-------------|-------|
| Whisper Large-v3 | Best open-source | Designed for long-form |
| Closed-source (Deepgram, etc.) | Better | Edge over open models |
| Distil-Large-v3.5 | Good | 25s optimal chunk |

---

## VRAM Consumption Benchmarks

### faster-whisper Models

| Model | float16 | int8_float16 | int8 |
|-------|---------|--------------|------|
| tiny | ~0.5GB | ~0.3GB | ~0.3GB |
| base | ~0.8GB | ~0.5GB | ~0.5GB |
| small | ~1.2GB | ~0.8GB | ~0.7GB |
| medium | ~2.5GB | ~1.5GB | ~1.3GB |
| large-v3 | ~5GB | ~3.5GB | ~3GB |
| large-v3-turbo | ~4.5GB | ~3GB | ~2.8GB |
| distil-large-v3.5 | ~2.4GB | ~1.5GB | ~1.3GB |

### NeMo Models (Estimated)

| Model | FP16 (est.) | INT8 (if supported) |
|-------|-------------|---------------------|
| Parakeet TDT 0.6B | ~2-3GB | ~1.5GB |
| Parakeet TDT 1.1B | ~4-5GB | ~2.5GB |
| Canary-Qwen-2.5B | ~5-6GB | ~3GB |

---

## Throughput Benchmarks (Batch Processing)

### Audio Processed Per Hour (RTX 3090 estimated)

| Model | Hours of Audio / Hour |
|-------|----------------------|
| Parakeet TDT 0.6B | ~3000 hours |
| Parakeet CTC 1.1B | ~2500 hours |
| faster-whisper large-v3-turbo | ~200 hours |
| faster-whisper distil-large-v3.5 | ~140 hours |
| faster-whisper large-v3 | ~70 hours |

---

## Comparison: faster-whisper vs Alternatives

### faster-whisper vs whisper.cpp

| Aspect | faster-whisper | whisper.cpp |
|--------|----------------|-------------|
| Speed (CPU) | Faster | Slower |
| Speed (GPU) | Faster | Comparable |
| Python Integration | Native | Bindings required |
| Memory Usage | Lower | Higher |
| Quality | Identical | May vary |

### faster-whisper vs insanely-fast-whisper

| Aspect | faster-whisper | insanely-fast-whisper |
|--------|----------------|----------------------|
| Speed | 4x OpenAI | 12-36x OpenAI |
| Hardware Req. | Modest GPU | High-end GPU (A100) |
| Ease of Use | Simple | Requires FlashAttention-2 |
| Best For | General use | Batch processing |

---

## Benchmark Methodology Notes

1. **WER Calculation:** Word Error Rate = (S + D + I) / N
   - S = Substitutions, D = Deletions, I = Insertions, N = Total words

2. **RTFx Calculation:** Audio duration / Processing time
   - Higher = faster
   - Measured on specific GPU (usually A100 for leaderboard)

3. **Variability Factors:**
   - Audio quality and length
   - GPU thermal throttling
   - CUDA/cuDNN versions
   - Batch size
   - Beam search settings

4. **Caveats:**
   - Benchmarks from different sources may not be directly comparable
   - Real-world performance varies from synthetic benchmarks
   - Leaderboard RTFx measured on datacenter GPUs (A100/H100)
