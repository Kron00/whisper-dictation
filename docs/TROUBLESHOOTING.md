# Troubleshooting Guide

Common issues and solutions for Whisper Dictation.

## Quick Diagnostics

Run these commands to check system status:

```bash
# Check if services are running
systemctl --user status whisper-daemon
systemctl --user status whisper-hotkey
systemctl --user status ydotoold

# Check daemon status
cat /tmp/whisper-daemon.status

# View recent daemon logs
journalctl --user -u whisper-daemon -n 50

# View recent hotkey logs
journalctl --user -u whisper-hotkey -n 50

# Check GPU status
nvidia-smi
```

## Service Issues

### Services Won't Start

**Symptoms**: Services show "failed" or "inactive" status

**Diagnosis**:
```bash
journalctl --user -u whisper-daemon -n 50
journalctl --user -u whisper-hotkey -n 50
```

**Common Causes**:

1. **Python 3.12 not found**
   ```bash
   which python3.12
   # If not found, install Python 3.12
   ```

2. **Virtual environment missing**
   ```bash
   ls ~/.local/share/whisper-dictation/bin/python3.12
   # If missing, run: ./install.sh
   ```

3. **CUDA libraries not found**
   - Check LD_LIBRARY_PATH in service file
   - Reinstall nemo_toolkit: `~/.local/share/whisper-dictation/bin/pip install --force-reinstall 'nemo_toolkit[asr]'`

### Services Crash Repeatedly

**Symptoms**: Services restart constantly, logs show errors

**Solution**:
```bash
# Stop the failing service
systemctl --user stop whisper-daemon

# Check for detailed errors
journalctl --user -u whisper-daemon -n 100

# Common fixes:
# 1. Clear CUDA cache
rm -rf ~/.cache/torch_extensions/

# 2. Clear model cache
rm -rf ~/.cache/huggingface/hub/models--nvidia--parakeet*

# 3. Reinstall Python packages
~/.local/share/whisper-dictation/bin/pip install --force-reinstall 'nemo_toolkit[asr]'
```

## GPU / CUDA Issues

### "CUDA out of memory"

**Symptoms**: Daemon crashes with OOM error

**Solution**:
1. Check VRAM usage: `nvidia-smi`
2. Close other GPU applications
3. Minimum 3GB VRAM required; 4GB+ recommended

### "CUDA not available" or "No CUDA devices"

**Symptoms**: Logs show CUDA not detected

**Diagnosis**:
```bash
# Check NVIDIA driver
nvidia-smi

# Check CUDA toolkit
nvcc --version

# Test PyTorch CUDA
~/.local/share/whisper-dictation/bin/python -c "import torch; print(torch.cuda.is_available())"
```

**Solution**:
- Install/update NVIDIA drivers
- Install CUDA toolkit
- Reinstall PyTorch with CUDA: `~/.local/share/whisper-dictation/bin/pip install --force-reinstall torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

### GPU Lock or Zombie Processes

**Symptoms**: nvidia-smi shows processes that won't die

**Solution**:
```bash
# Find and kill zombie processes
nvidia-smi
# Note the PID of whisper-daemon
sudo kill -9 <PID>

# Restart services
systemctl --user restart whisper-daemon
```

## Audio Issues

### No Audio Recording / Silent Transcriptions

**Symptoms**: Recording happens but produces no text or "[BLANK]"

**Diagnosis**:
```bash
# Test microphone
pw-record --list-targets
# Should show your microphone

# Test recording manually
pw-record -P '{ "stream.capture.sink": false }' test.wav
# Speak for a few seconds, then Ctrl+C
# Play it back: pw-play test.wav
```

**Solutions**:

1. **Wrong audio device selected** - whisper-dictate defaults to first audio source
   - Edit `~/.local/bin/whisper-dictate`
   - Find the `pw-record` line and add device selector

2. **Microphone muted**
   - Check pavucontrol or GNOME Sound Settings
   - Ensure microphone is not muted

3. **PipeWire not running**
   ```bash
   systemctl --user status pipewire
   systemctl --user start pipewire
   ```

### Audio Distorted / Choppy

**Symptoms**: Recording sounds distorted or skips

**Solution**:
1. Check sample rate: `pw-metadata -n settings`
2. Adjust buffer size in PipeWire config
3. Close other audio applications

## Hotkey / Double-Click Issues

### Double-Click Not Detected

**Symptoms**: Nothing happens when you double middle-click

**Diagnosis**:
```bash
# Check hotkey service logs
journalctl --user -u whisper-hotkey -f

# Then try double middle-click - should see log entries
```

**Solutions**:

1. **Wrong mouse device**
   - The script looks for "Logitech USB Receiver" by default
   - Edit `~/.local/bin/whisper-hotkey` and change `DEVICE_PATTERN` to match your mouse
   - Find your device: `ls /dev/input/by-id/`

2. **Permission denied on /dev/input**
   ```bash
   # Add user to input group
   sudo usermod -a -G input $USER
   # Log out and back in
   ```

3. **ydotoold not running**
   ```bash
   systemctl --user status ydotoold
   systemctl --user start ydotoold
   ```

### Accidental Triggers / Too Sensitive

**Symptoms**: Records when you don't want it to

**Solution**: Adjust double-click threshold
- Edit `~/.local/bin/whisper-hotkey`
- Change `DOUBLE_CLICK_THRESHOLD` (default: 0.3 seconds)
- Increase for slower double-clicks, decrease for faster

## Transcription Issues

### Poor Accuracy / Wrong Words

**Symptoms**: Transcribed text is incorrect

**Causes**:
1. **Background noise** - Use noise reduction (see CONFIGURATION.md)
2. **Microphone too far** - Optimal distance: 6-12 inches
3. **Audio gain too low** - Use auto-gain feature
4. **Speaking too fast** - Speak clearly at normal pace

**Solutions**:
```bash
# Enable noise reduction
touch /tmp/whisper-noise-reduction.enabled

# Use auto-gain (if whisper-autogain is installed)
whisper-autogain learn

# Check audio levels during recording
whisper-stream
# Speak and observe volume levels
```

### Transcription Slow / Takes Long Time

**Symptoms**: Long pause after recording before text appears

**Possible Causes**:
1. **Model not loaded in VRAM** (first use only)
2. **GPU busy with other processes**
3. **Long recording** (expected - transcription takes ~10% of recording time)

**Solutions**:
```bash
# Check daemon status
cat /tmp/whisper-daemon.status
# Should show "ready"

# Check GPU usage
nvidia-smi
# VRAM should show ~2-3GB used by whisper-daemon

# Restart daemon to reload model
systemctl --user restart whisper-daemon
```

### "Connection refused" Error

**Symptoms**: Logs show socket connection errors

**Solution**:
```bash
# Check if daemon is running
systemctl --user status whisper-daemon

# Check socket exists
ls -la /tmp/whisper-daemon.sock

# Restart daemon
systemctl --user restart whisper-daemon
```

## Text Pasting Issues

### Text Doesn't Paste

**Symptoms**: Recording works but text doesn't appear

**Diagnosis**:
```bash
# Check if text is in clipboard
wl-paste
# Should show the transcribed text
```

**Solutions**:

1. **wl-clipboard not installed**
   ```bash
   # Fedora
   sudo dnf install wl-clipboard
   ```

2. **ydotool not working**
   ```bash
   # Test ydotool manually
   echo "test" | ydotool type --file -
   # Should type "test"

   # Check ydotoold service
   systemctl --user status ydotoold
   ```

3. **Wrong paste command**
   - Default: Ctrl+Shift+V (plain text)
   - If your app needs Ctrl+V, edit `~/.local/bin/whisper-dictate`

## Statistics / WhisperStats Issues

### WhisperStats Won't Launch

**Symptoms**: Error when running `whisperstats`

**Diagnosis**:
```bash
# Run manually to see errors
~/.local/share/whisper-dictation/bin/python ~/.local/bin/whisperstats
```

**Solutions**:

1. **GTK4 not installed**
   ```bash
   # Fedora
   sudo dnf install gtk4 libadwaita
   ```

2. **Python GTK bindings missing**
   ```bash
   # Fedora
   sudo dnf install python3-gobject
   ```

3. **Database corrupt**
   ```bash
   # Backup and reset
   mv ~/.local/share/whisper-dictation/stats.db ~/.local/share/whisper-dictation/stats.db.bak
   # Stats will be recreated on next use
   ```

## Performance Issues

### High CPU Usage

**Symptoms**: CPU at 100% during idle

**Causes**:
- Daemon shouldn't use CPU when idle
- Check for runaway processes

**Solution**:
```bash
# Check what's using CPU
top
# Look for whisper processes

# Restart services
systemctl --user restart whisper-daemon whisper-hotkey
```

### High VRAM Usage

**Symptoms**: GPU memory not freed after use

**This is normal**: The daemon keeps the model loaded in VRAM for instant transcription. This is by design.

To free VRAM:
```bash
systemctl --user stop whisper-daemon
```

## Model Download Issues

### Model Won't Download

**Symptoms**: Daemon stuck at "starting", model not downloading

**Diagnosis**:
```bash
journalctl --user -u whisper-daemon -f
# Should show download progress
```

**Solutions**:

1. **Network issues**
   - Check internet connection
   - Try manual download: `huggingface-cli download nvidia/parakeet-tdt-0.6b`

2. **Disk space full**
   ```bash
   df -h ~/.cache/huggingface
   # Need ~8GB free space
   ```

3. **Firewall blocking HuggingFace**
   - Check firewall settings
   - Try: `curl -I https://huggingface.co`

## Permission Issues

### "Permission denied" Errors

**Common permission issues**:

1. **evdev access**
   ```bash
   sudo usermod -a -G input $USER
   # Log out and back in
   ```

2. **ydotool socket**
   ```bash
   ls -la /run/user/$UID/ydotool.socket
   # Should show user ownership
   ```

3. **Script permissions**
   ```bash
   chmod +x ~/.local/bin/whisper-*
   chmod +x ~/.local/bin/whisperstats
   ```

## Still Having Issues?

If none of these solutions work:

1. **Collect logs**:
   ```bash
   journalctl --user -u whisper-daemon -n 100 > daemon.log
   journalctl --user -u whisper-hotkey -n 100 > hotkey.log
   systemctl --user status whisper-daemon > daemon-status.txt
   nvidia-smi > gpu-info.txt
   ```

2. **Open an issue** on GitHub with:
   - Description of the problem
   - Steps to reproduce
   - Log files attached
   - System info (distro, GPU, Python version)

3. **Check existing issues** on GitHub - your problem might already be solved
