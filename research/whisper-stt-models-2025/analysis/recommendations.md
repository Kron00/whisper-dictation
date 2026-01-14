# Final Ranked Recommendations

## Your Use Case Summary
- **Hardware:** RTX 3090 (24GB VRAM)
- **Current Setup:** faster-whisper + distil-large-v3.5-ct2 + int8_float16
- **Need:** Fast transcription for real-time dictation
- **Language:** English only

---

## Tier 1: Recommended (Stay with faster-whisper)

### Rank 1: distil-whisper/distil-large-v3.5-ct2 [CURRENT - KEEP]

| Attribute | Value |
|-----------|-------|
| **Model** | `distil-whisper/distil-large-v3.5-ct2` |
| **Source** | https://huggingface.co/distil-whisper/distil-large-v3.5-ct2 |
| **Speed** | RTFx ~140 (fastest in faster-whisper family) |
| **Accuracy** | WER ~7-8% (within 1% of large-v3) |
| **VRAM** | ~1.5GB (int8_float16) |
| **Works with faster-whisper** | Yes |
| **Recommendation** | **KEEP - This is the optimal choice for your use case** |

**Why keep this:**
- Best speed-to-accuracy ratio in faster-whisper ecosystem
- 1.5x faster than large-v3-turbo
- Minimal VRAM usage leaves room for other applications
- Well-tested, stable, community-supported
- Your int8_float16 quantization is optimal

---

### Rank 2: deepdml/faster-whisper-large-v3-turbo-ct2 [ALTERNATIVE]

| Attribute | Value |
|-----------|-------|
| **Model** | `deepdml/faster-whisper-large-v3-turbo-ct2` |
| **Source** | https://huggingface.co/deepdml/faster-whisper-large-v3-turbo-ct2 |
| **Speed** | RTFx ~90 (1.5x slower than distil-v3.5) |
| **Accuracy** | WER ~6.5% (~1% better than distil) |
| **VRAM** | ~3GB (int8_float16) |
| **Works with faster-whisper** | Yes |
| **Recommendation** | Consider if you need maximum accuracy within faster-whisper |

**When to switch:**
- If you notice transcription errors with distil-v3.5
- For applications where accuracy trumps speed
- VRAM increase (1.5GB -> 3GB) is negligible on your RTX 3090

**Usage:**
```python
from faster_whisper import WhisperModel

model = WhisperModel(
    "deepdml/faster-whisper-large-v3-turbo-ct2",
    device="cuda",
    compute_type="int8_float16"
)
```

---

### Rank 3: Systran/faster-whisper-large-v3 [ACCURACY PRIORITY]

| Attribute | Value |
|-----------|-------|
| **Model** | `Systran/faster-whisper-large-v3` |
| **Source** | https://huggingface.co/Systran/faster-whisper-large-v3 |
| **Speed** | RTFx ~68 (2x slower than distil) |
| **Accuracy** | WER ~6.4% (best in faster-whisper) |
| **VRAM** | ~3.5-4GB (int8_float16) |
| **Works with faster-whisper** | Yes |
| **Recommendation** | Only if maximum accuracy is required |

---

## Tier 2: Alternative Frameworks (Significant Performance Gains)

### Rank 4: nvidia/parakeet-tdt-0.6b-v2 [BEST OVERALL]

| Attribute | Value |
|-----------|-------|
| **Model** | `nvidia/parakeet-tdt-0.6b-v2` |
| **Source** | https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2 |
| **Speed** | RTFx 3386 (50x faster than Whisper) |
| **Accuracy** | WER 6.05% (better than any Whisper) |
| **VRAM** | ~2-3GB |
| **Works with faster-whisper** | **NO - Requires NeMo** |
| **Recommendation** | **Best option if willing to switch frameworks** |

**Why consider:**
- Objectively the best open-source ASR for English
- 50x faster AND more accurate than your current setup
- Word-level timestamps built-in
- Punctuation and capitalization included

**Trade-offs:**
- Requires learning NeMo framework
- Different API than faster-whisper
- English-only (not an issue for you)

**Quick test:**
```bash
pip install 'nemo_toolkit[asr]==2.4.0'
```
```python
import nemo.collections.asr as nemo_asr
model = nemo_asr.models.ASRModel.from_pretrained("nvidia/parakeet-tdt-0.6b-v2")
print(model.transcribe(["test.wav"]))
```

---

### Rank 5: nvidia/canary-qwen-2.5b [HIGHEST ACCURACY]

| Attribute | Value |
|-----------|-------|
| **Model** | `nvidia/canary-qwen-2.5b` |
| **Source** | https://huggingface.co/nvidia/canary-qwen-2.5b |
| **Speed** | RTFx 418 (3x faster than Whisper large-v3) |
| **Accuracy** | WER 5.63% (BEST on Open ASR Leaderboard) |
| **VRAM** | ~5-6GB |
| **Works with faster-whisper** | **NO - Requires NeMo** |
| **Recommendation** | For absolute maximum accuracy |

---

### Rank 6: kyutai/stt-2.6b-en [BEST STREAMING]

| Attribute | Value |
|-----------|-------|
| **Model** | `kyutai/stt-2.6b-en` |
| **Source** | https://huggingface.co/kyutai/stt-2.6b-en |
| **Speed** | 2.5s initial latency, then real-time |
| **Accuracy** | WER 6.4% |
| **VRAM** | ~6-8GB |
| **Works with faster-whisper** | **NO - Requires Moshi/PyTorch** |
| **Recommendation** | For true streaming applications |

**Why consider:**
- Native streaming (not chunk-based like Whisper)
- Very low latency after initial warmup
- Good accuracy

---

## Tier 3: Specialized Use Cases

### Rank 7: nvidia/parakeet-tdt-1.1b [BETTER ACCURACY, MORE VRAM]

| Attribute | Value |
|-----------|-------|
| **Speed** | RTFx ~2000 |
| **Accuracy** | WER <7% |
| **VRAM** | ~4-5GB |
| **Recommendation** | If 0.6B accuracy isn't sufficient |

### Rank 8: UsefulSensors/moonshine [EDGE DEVICES]

| Attribute | Value |
|-----------|-------|
| **Speed** | 5-15x faster than Whisper tiny |
| **Accuracy** | WER ~12% |
| **VRAM** | <1GB |
| **Recommendation** | Only for embedded/edge deployments |

---

## Decision Matrix

| Priority | Recommendation |
|----------|----------------|
| "It works, don't fix it" | Keep distil-large-v3.5-ct2 |
| Slightly better accuracy, same framework | Try large-v3-turbo-ct2 |
| Maximum speed AND accuracy | Switch to Parakeet TDT 0.6B v2 |
| Highest possible accuracy | Switch to Canary-Qwen-2.5B |
| True streaming with low latency | Try Kyutai STT 2.6B |

---

## Final Verdict

**For your specific use case (real-time dictation on RTX 3090):**

### Option A: Stay with faster-whisper (Recommended if current setup is satisfactory)
```python
# Your current setup - OPTIMAL
from faster_whisper import WhisperModel

model = WhisperModel(
    "distil-whisper/distil-large-v3.5-ct2",
    device="cuda",
    compute_type="int8_float16"
)
```

### Option B: Upgrade to Parakeet (Recommended for maximum performance)
```python
# 50x faster + better accuracy
import nemo.collections.asr as nemo_asr

model = nemo_asr.models.ASRModel.from_pretrained("nvidia/parakeet-tdt-0.6b-v2")
```

**My recommendation:** Try Parakeet TDT 0.6B v2 as a test. If the NeMo framework integration works well with your dictation pipeline, it offers objectively superior performance. If the framework switch is too disruptive, your current faster-whisper setup with distil-large-v3.5-ct2 is already excellent and among the best options within that ecosystem.
