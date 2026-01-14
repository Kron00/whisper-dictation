# Plan: Auto-Adjusting Microphone Volume for Whisper Dictation

## Goal
Create a fully autonomous microphone volume optimization system that:
- Runs invisibly in the background (no user interaction needed)
- Learns optimal levels over time based on actual recordings
- Adjusts automatically if audio is too loud (clipping) or too quiet
- Persists settings across sessions

## How It Works

### Concept: Adaptive Learning Loop
```
[Start Recording] → [Save current volume] → [Apply optimal volume]
       ↓
[User speaks and recording happens normally]
       ↓
[After recording] → [Restore original volume] → [Analyze audio & learn]
       ↓
[Too loud?] → Lower saved volume for next time
[Too quiet?] → Raise saved volume for next time
[Just right?] → Keep current setting
```

### Volume Restore (for Discord, etc.)
The system saves your current mic volume before recording and restores it after:
- On Discord at 80% → Whisper sets to 65% → Records → Restores to 80%
- Your Discord/other apps continue working at their expected volume

### Audio Level Targets
- **Optimal peak**: -12dB to -6dB (70-90% of max without clipping)
- **Too quiet**: Below -20dB peak (needs volume increase)
- **Too loud/clipping**: Above -3dB or detected clipping (needs decrease)

## Implementation

### New File: `~/.local/bin/whisper-autogain`
Python script that handles volume analysis and adjustment.

```python
#!/usr/bin/env python3
"""Auto-gain control for whisper dictation - runs invisibly."""

Functions:
- get_current_volume() → float (0.0-1.0)
- set_volume(level: float) → None
- analyze_audio(wav_path) → dict with peak_db, rms_db, clipping_detected
- load_optimal_volume() → float (from persistent file)
- save_optimal_volume(level: float) → None
- calculate_adjustment(analysis) → float (new optimal level)
- apply_optimal_volume() → None (called before recording)
- learn_from_recording(wav_path) → None (called after recording)
```

### Config File: `~/.config/whisper-dictation/autogain.json`
```json
{
  "optimal_volume": 0.70,
  "last_analysis": {
    "peak_db": -8.5,
    "rms_db": -18.2,
    "clipping": false
  }
}
```

### Temp File: `/tmp/whisper-autogain-restore`
Stores the user's original volume to restore after recording:
```
0.80
```

### Integration Points in `whisper-dictate`

**Before recording starts (line ~247):**
```bash
# Save current volume and apply optimal for recording
[[ -x "$AUTOGAIN_SCRIPT" ]] && "$AUTOGAIN_SCRIPT" apply 2>/dev/null
```

**After recording completes, before cleanup (around line ~303):**
```bash
# Restore original volume immediately (so Discord etc. work right away)
[[ -x "$AUTOGAIN_SCRIPT" ]] && "$AUTOGAIN_SCRIPT" restore 2>/dev/null

# Learn from this recording in background (doesn't block paste)
[[ -x "$AUTOGAIN_SCRIPT" ]] && "$AUTOGAIN_SCRIPT" learn "$AUDIO_FILE" &>/dev/null &
```

## Detailed Implementation

### 1. whisper-autogain script

```python
#!/usr/bin/env python3
"""Autonomous microphone gain control for whisper dictation."""
import json
import subprocess
import sys
import wave
import struct
import math
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "whisper-dictation"
CONFIG_FILE = CONFIG_DIR / "autogain.json"
RESTORE_FILE = Path("/tmp/whisper-autogain-restore")

# Target levels (in dB)
TARGET_PEAK_DB = -9.0      # Ideal peak level
MIN_PEAK_DB = -20.0        # Too quiet threshold
MAX_PEAK_DB = -3.0         # Too loud threshold
ADJUSTMENT_STEP = 0.05     # 5% adjustment per learning cycle
MIN_VOLUME = 0.30          # Never go below 30%
MAX_VOLUME = 1.00          # Never exceed 100%
DEFAULT_VOLUME = 0.70      # Starting point

def get_current_volume():
    """Get current mic volume via wpctl."""
    result = subprocess.run(
        ["wpctl", "get-volume", "@DEFAULT_AUDIO_SOURCE@"],
        capture_output=True, text=True
    )
    # Output: "Volume: 0.80"
    return float(result.stdout.split()[-1])

def set_volume(level):
    """Set mic volume via wpctl."""
    level = max(MIN_VOLUME, min(MAX_VOLUME, level))
    subprocess.run(
        ["wpctl", "set-volume", "@DEFAULT_AUDIO_SOURCE@", str(level)],
        capture_output=True
    )

def analyze_audio(wav_path):
    """Analyze audio file for peak and RMS levels."""
    with wave.open(wav_path, 'rb') as wf:
        n_frames = wf.getnframes()
        if n_frames == 0:
            return None

        frames = wf.readframes(n_frames)
        samples = struct.unpack(f'{n_frames}h', frames)

        # Calculate peak
        peak = max(abs(s) for s in samples)
        peak_ratio = peak / 32768.0
        peak_db = 20 * math.log10(peak_ratio) if peak_ratio > 0 else -96

        # Calculate RMS
        rms = math.sqrt(sum(s**2 for s in samples) / n_frames)
        rms_ratio = rms / 32768.0
        rms_db = 20 * math.log10(rms_ratio) if rms_ratio > 0 else -96

        # Detect clipping (samples at max value)
        clipping = peak >= 32760

        return {
            "peak_db": peak_db,
            "rms_db": rms_db,
            "clipping": clipping
        }

def load_config():
    """Load config, creating defaults if needed."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {"optimal_volume": DEFAULT_VOLUME}

def save_config(config):
    """Save config to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2))

def cmd_apply():
    """Save current volume, then apply optimal for recording."""
    # Save current volume so we can restore it later
    current = get_current_volume()
    RESTORE_FILE.write_text(str(current))

    # Apply optimal recording volume
    config = load_config()
    optimal = config.get("optimal_volume", DEFAULT_VOLUME)
    set_volume(optimal)

def cmd_restore():
    """Restore the original volume (for Discord, etc.)."""
    if RESTORE_FILE.exists():
        try:
            original = float(RESTORE_FILE.read_text().strip())
            set_volume(original)
            RESTORE_FILE.unlink()  # Clean up
        except (ValueError, OSError):
            pass

def cmd_learn(wav_path):
    """Learn from a recording and adjust optimal volume."""
    analysis = analyze_audio(wav_path)
    if not analysis:
        return

    config = load_config()
    current_optimal = config.get("optimal_volume", DEFAULT_VOLUME)

    # Determine adjustment
    if analysis["clipping"] or analysis["peak_db"] > MAX_PEAK_DB:
        # Too loud - decrease
        new_optimal = current_optimal - ADJUSTMENT_STEP
    elif analysis["peak_db"] < MIN_PEAK_DB:
        # Too quiet - increase
        new_optimal = current_optimal + ADJUSTMENT_STEP
    else:
        # Good level - no change
        new_optimal = current_optimal

    # Clamp to valid range
    new_optimal = max(MIN_VOLUME, min(MAX_VOLUME, new_optimal))

    # Save
    config["optimal_volume"] = new_optimal
    config["last_analysis"] = analysis
    save_config(config)

def cmd_status():
    """Show current status."""
    config = load_config()
    current = get_current_volume()
    print(f"Current mic volume: {current:.0%}")
    print(f"Saved optimal: {config.get('optimal_volume', DEFAULT_VOLUME):.0%}")
    if "last_analysis" in config:
        a = config["last_analysis"]
        print(f"Last recording: peak={a['peak_db']:.1f}dB, clipping={a['clipping']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        cmd_status()
    elif sys.argv[1] == "apply":
        cmd_apply()
    elif sys.argv[1] == "restore":
        cmd_restore()
    elif sys.argv[1] == "learn" and len(sys.argv) > 2:
        cmd_learn(sys.argv[2])
    elif sys.argv[1] == "status":
        cmd_status()
    else:
        print("Usage: whisper-autogain [apply|restore|learn <wav>|status]")
```

### 2. Modifications to whisper-dictate

**Add near top (after variable declarations):**
```bash
AUTOGAIN_SCRIPT="$HOME/.local/bin/whisper-autogain"
```

**In start_recording(), before pw-record (around line 247):**
```bash
# Apply optimal microphone volume (invisible to user)
[[ -x "$AUTOGAIN_SCRIPT" ]] && "$AUTOGAIN_SCRIPT" apply 2>/dev/null
```

**In stop_and_transcribe(), after transcription but before cleanup:**
```bash
# Restore original volume immediately (so Discord etc. work right away)
[[ -x "$AUTOGAIN_SCRIPT" ]] && "$AUTOGAIN_SCRIPT" restore 2>/dev/null

# Learn from this recording in background (doesn't block paste)
[[ -x "$AUTOGAIN_SCRIPT" ]] && "$AUTOGAIN_SCRIPT" learn "$AUDIO_FILE" &>/dev/null &
```

## Files to Create/Modify

| File | Action | Description |
|------|--------|-------------|
| `~/.local/bin/whisper-autogain` | **Create** | New Python script for volume control |
| `~/.local/bin/whisper-dictate` | **Modify** | Add apply/restore/learn hooks |
| `~/.config/whisper-dictation/autogain.json` | **Auto-created** | Persistent config (created by script) |

## User Experience

1. **First use**: Starts at 70% volume (sensible default)
2. **Speaks too quietly**: Next recording bumps up 5%
3. **Speaks too loudly/clips**: Next recording reduces 5%
4. **After a few uses**: Converges to optimal level for their voice/mic
5. **User notices nothing**: Just works better over time

### Discord/Other Apps Scenario
1. User on Discord at 80% mic volume
2. Double-click to dictate → Volume saved (80%), set to optimal (65%)
3. User speaks, recording happens
4. Recording ends → Volume restored to 80% immediately
5. Discord continues working perfectly at 80%
6. Learning happens in background (adjusts 65% if needed for next time)

## Edge Cases Handled

- **Empty/silent recording**: Skip learning (no adjustment)
- **Config file missing**: Use defaults
- **wpctl not available**: Fail silently (script is optional)
- **Learning runs async**: Doesn't delay the paste operation
- **Volume restore on crash**: Temp file cleaned up, worst case user manually adjusts
