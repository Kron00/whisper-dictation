# HuggingFace Model Links and Details

## Official faster-whisper Compatible Models

### Systran Official Models
| Model | URL | Description |
|-------|-----|-------------|
| faster-whisper-tiny | https://huggingface.co/Systran/faster-whisper-tiny | 39M params |
| faster-whisper-tiny.en | https://huggingface.co/Systran/faster-whisper-tiny.en | English-only |
| faster-whisper-base | https://huggingface.co/Systran/faster-whisper-base | 74M params |
| faster-whisper-base.en | https://huggingface.co/Systran/faster-whisper-base.en | English-only |
| faster-whisper-small | https://huggingface.co/Systran/faster-whisper-small | 244M params |
| faster-whisper-small.en | https://huggingface.co/Systran/faster-whisper-small.en | English-only |
| faster-whisper-medium | https://huggingface.co/Systran/faster-whisper-medium | 769M params |
| faster-whisper-medium.en | https://huggingface.co/Systran/faster-whisper-medium.en | English-only |
| faster-whisper-large-v1 | https://huggingface.co/Systran/faster-whisper-large-v1 | 1.55B params |
| faster-whisper-large-v2 | https://huggingface.co/Systran/faster-whisper-large-v2 | 1.55B params |
| faster-whisper-large-v3 | https://huggingface.co/Systran/faster-whisper-large-v3 | 1.55B params |
| faster-distil-whisper-large-v2 | https://huggingface.co/Systran/faster-distil-whisper-large-v2 | Distilled v2 |

### Distil-Whisper Official Models
| Model | URL | Description |
|-------|-----|-------------|
| **distil-large-v3.5** | https://huggingface.co/distil-whisper/distil-large-v3.5 | Latest, 0.8B params |
| **distil-large-v3.5-ct2** | https://huggingface.co/distil-whisper/distil-large-v3.5-ct2 | CTranslate2 format |
| distil-large-v3.5-openai | https://huggingface.co/distil-whisper/distil-large-v3.5-openai | OpenAI format |
| distil-large-v3.5-ONNX | https://huggingface.co/distil-whisper/distil-large-v3.5-ONNX | ONNX format |
| distil-large-v3.5-ggml | https://huggingface.co/distil-whisper/distil-large-v3.5-ggml | GGML format |
| distil-large-v3 | https://huggingface.co/distil-whisper/distil-large-v3 | Previous version |
| distil-large-v3-ct2 | https://huggingface.co/distil-whisper/distil-large-v3-ct2 | CTranslate2 format |

### Community CTranslate2 Conversions
| Model | URL | Description |
|-------|-----|-------------|
| **faster-whisper-large-v3-turbo-ct2** | https://huggingface.co/deepdml/faster-whisper-large-v3-turbo-ct2 | Turbo in CT2 |
| faster-distil-whisper-large-v3.5 | https://huggingface.co/deepdml/faster-distil-whisper-large-v3.5 | Alt distil-v3.5 |
| faster-distil-whisper-large-v3.5 | https://huggingface.co/Purfview/faster-distil-whisper-large-v3.5 | Purfview version |

---

## OpenAI Official Whisper Models

| Model | URL | Params | Description |
|-------|-----|--------|-------------|
| whisper-tiny | https://huggingface.co/openai/whisper-tiny | 39M | Smallest |
| whisper-base | https://huggingface.co/openai/whisper-base | 74M | Basic |
| whisper-small | https://huggingface.co/openai/whisper-small | 244M | Small |
| whisper-medium | https://huggingface.co/openai/whisper-medium | 769M | Medium |
| whisper-large | https://huggingface.co/openai/whisper-large | 1.55B | Large v1 |
| whisper-large-v2 | https://huggingface.co/openai/whisper-large-v2 | 1.55B | Large v2 |
| whisper-large-v3 | https://huggingface.co/openai/whisper-large-v3 | 1.55B | Large v3 |
| **whisper-large-v3-turbo** | https://huggingface.co/openai/whisper-large-v3-turbo | 809M | Latest turbo |

---

## NVIDIA NeMo Models

### Parakeet Family
| Model | URL | Params | WER | RTFx |
|-------|-----|--------|-----|------|
| **parakeet-tdt-0.6b-v2** | https://huggingface.co/nvidia/parakeet-tdt-0.6b-v2 | 600M | 6.05% | 3386 |
| parakeet-tdt-0.6b-v3 | https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3 | 600M | ~6% | 3386 |
| parakeet-tdt-1.1b | https://huggingface.co/nvidia/parakeet-tdt-1.1b | 1.1B | <7% | ~2000 |
| parakeet-ctc-1.1b | https://huggingface.co/nvidia/parakeet-ctc-1.1b | 1.1B | 6.68% | 2793 |
| parakeet-rnnt-1.1b | https://huggingface.co/nvidia/parakeet-rnnt-1.1b | 1.1B | ~7% | ~1200 |

### Canary Family
| Model | URL | Params | WER | RTFx |
|-------|-----|--------|-----|------|
| **canary-qwen-2.5b** | https://huggingface.co/nvidia/canary-qwen-2.5b | 2.5B | 5.63% | 418 |
| canary-1b-v2 | https://huggingface.co/nvidia/canary-1b-v2 | 1B | ~7% | ~1000 |
| canary-1b-flash | https://huggingface.co/nvidia/canary-1b-flash | 1B | ~7.5% | >1000 |

---

## Kyutai/Moshi Models

| Model | URL | Params | Description |
|-------|-----|--------|-------------|
| **stt-2.6b-en** | https://huggingface.co/kyutai/stt-2.6b-en | 2.6B | English-only, 2.5s latency |
| stt-1b-en_fr | https://huggingface.co/kyutai/stt-1b-en_fr | 1B | EN+FR, 0.5s latency |

---

## IBM Granite Speech Models

| Model | URL | Params | Description |
|-------|-----|--------|-------------|
| granite-speech-3.3-8b | https://huggingface.co/ibm-granite/granite-speech-3.3-8b | 8B | Full model |
| granite-speech-3.3-2b | https://huggingface.co/ibm-granite/granite-speech-3.3-2b | 2B | Compact version |

---

## Moonshine Models

| Model | URL | Params | Description |
|-------|-----|--------|-------------|
| moonshine | https://huggingface.co/UsefulSensors/moonshine | ~27M-100M | Edge-optimized |

---

## Fine-Tuned Specialty Models

| Model | URL | Specialty |
|-------|-----|-----------|
| whisper-medium.en-fine-tuned-for-ATC | https://huggingface.co/jacktol/whisper-medium.en-fine-tuned-for-ATC | Air Traffic Control |
| whisper-medium.en-fine-tuned-for-ATC-faster-whisper | https://huggingface.co/jacktol/whisper-medium.en-fine-tuned-for-ATC-faster-whisper | ATC (CT2) |

---

## GitHub Repositories

| Repository | URL | Description |
|------------|-----|-------------|
| faster-whisper | https://github.com/SYSTRAN/faster-whisper | CTranslate2 implementation |
| distil-whisper | https://github.com/huggingface/distil-whisper | Distillation codebase |
| openai/whisper | https://github.com/openai/whisper | Original OpenAI repo |
| whisper.cpp | https://github.com/ggml-org/whisper.cpp | C++ implementation |
| RealtimeSTT | https://github.com/KoljaB/RealtimeSTT | Real-time library |
| WhisperLive | https://github.com/collabora/WhisperLive | Near-live implementation |
| NeMo | https://github.com/NVIDIA/NeMo | NVIDIA NeMo toolkit |
| Moshi | https://github.com/kyutai-labs/moshi | Kyutai framework |

---

## Open ASR Leaderboard

- **URL:** https://huggingface.co/spaces/hf-audio/open_asr_leaderboard
- **GitHub:** https://github.com/huggingface/open_asr_leaderboard
- **Description:** Benchmarks 60+ models from 18 organizations across 11 datasets
- **Updated:** November 2025

---

## Installation Commands

### faster-whisper
```bash
pip install faster-whisper
```

### NVIDIA NeMo (for Parakeet/Canary)
```bash
pip install 'nemo_toolkit[asr]==2.4.0'
```

### Kyutai/Moshi
```bash
pip install -U moshi          # PyTorch
pip install -U moshi_mlx      # Apple MLX
```

### whisper.cpp
```bash
git clone https://github.com/ggml-org/whisper.cpp.git
cd whisper.cpp
make
```
