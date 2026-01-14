# Plan: Pause Audio During Recording

## Goal
Automatically pause any playing audio (music, videos, etc.) when recording starts, and resume when recording stops.

## Approach Options

### Option 1: playerctl (Recommended)
Uses MPRIS D-Bus interface to control media players.

**Pros:**
- Works with Spotify, Firefox, Chrome, VLC, mpv, and most media players
- Can remember which players were playing and resume only those
- Clean, standard interface

**Cons:**
- Only works with MPRIS-compliant players
- Won't pause system sounds or non-MPRIS apps

**Implementation:**
```bash
# Pause all players
playerctl --all-players pause

# Resume all players
playerctl --all-players play
```

### Option 2: PipeWire Stream Corking
Directly cork (pause) audio streams at the PipeWire level.

**Pros:**
- Works with ALL audio, including system sounds
- Lower level, more complete

**Cons:**
- More complex to implement
- Harder to resume only previously-playing streams
- May interfere with recording

### Option 3: Hybrid Approach
Use playerctl for media players + mute system audio.

---

## Recommended Implementation (Option 1: playerctl)

### Changes to whisper-dictate

```bash
# Add at top
PAUSED_PLAYERS_FILE="/tmp/whisper-paused-players"

pause_audio() {
    # Get list of currently playing players
    playerctl --all-players --format '{{playerName}}' status 2>/dev/null | \
        grep -B1 "Playing" | grep -v "Playing" | grep -v "^--$" > "$PAUSED_PLAYERS_FILE" || true

    # Pause all
    playerctl --all-players pause 2>/dev/null || true
}

resume_audio() {
    if [[ -f "$PAUSED_PLAYERS_FILE" ]]; then
        while read -r player; do
            playerctl --player="$player" play 2>/dev/null || true
        done < "$PAUSED_PLAYERS_FILE"
        rm -f "$PAUSED_PLAYERS_FILE"
    fi
}
```

### Integration Points

1. **start_recording()** - Add `pause_audio` call
2. **stop_and_transcribe()** - Add `resume_audio` call after transcription
3. **cleanup()** - Add resume and file cleanup

### Simpler Alternative

If tracking which players were playing is too complex, just pause all and let user manually resume:

```bash
pause_audio() {
    playerctl --all-players pause 2>/dev/null || true
}

# No resume - user controls manually
```

---

## Dependencies

```bash
# Fedora
sudo dnf install playerctl
```

---

## Testing

```bash
# List players
playerctl --list-all

# Check status
playerctl --all-players status

# Test pause/play
playerctl --all-players pause
playerctl --all-players play
```

---

## Edge Cases

1. **No players running** - playerctl exits cleanly, no error
2. **Player starts during recording** - Won't be tracked, but also won't be paused
3. **Multiple players** - All paused, only previously-playing ones resumed
4. **Player closed during recording** - Resume fails silently, no issue

---

## Implementation Steps

1. Install playerctl
2. Add pause/resume functions to whisper-dictate
3. Call pause_audio in start_recording()
4. Call resume_audio in stop_and_transcribe() (after transcription completes)
5. Add cleanup to cleanup() function
6. Test with Spotify, Firefox, etc.
