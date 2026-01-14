# Installation Guide

Complete installation instructions for the Whisper Dictation system on Linux.

## Prerequisites

### Required Hardware

- **NVIDIA GPU** with at least 3GB VRAM (recommended: 4GB+)
  - Tested on: RTX 3090 (24GB), RTX 3060 Ti (8GB)
  - Minimum: GTX 1060 (6GB) or equivalent
- **Disk space**: ~8GB (including model cache)

### Required Software

- **Linux Distribution**: Fedora, Ubuntu, Arch Linux (or derivatives)
- **Desktop Environment**: Wayland (GNOME recommended)
  - X11 may work but is not officially supported
- **Python 3.12**
- **NVIDIA Drivers** with CUDA support (version 470+ recommended)
- **PipeWire audio system** (default on modern Linux)

### Quick Prerequisites Check

```bash
# Check NVIDIA GPU
nvidia-smi

# Check Python 3.12
python3.12 --version

# Check CUDA
nvcc --version  # Optional but recommended

# Check Wayland
echo $XDG_SESSION_TYPE  # Should output "wayland"
```

## Quick Installation

For most users, the automated installer is the easiest way to get started:

```bash
git clone https://github.com/Kron00/whisper-dictation.git
cd whisper-dictation
./install.sh
```

The installer will:
1. Check prerequisites (GPU, Python 3.12, CUDA)
2. Detect your distribution
3. Install system dependencies
4. Create Python virtual environment
5. Install Python packages (~5-10 minutes)
6. Install scripts to `~/.local/bin/`
7. Install and start systemd services
8. Validate the installation

## Manual Installation

If you prefer to install manually or need more control:

### 1. Clone Repository

```bash
git clone https://github.com/Kron00/whisper-dictation.git
cd whisper-dictation
```

### 2. Install System Dependencies

#### Fedora

```bash
sudo dnf install ydotool wl-clipboard playerctl python3-evdev python3-gobject gtk4 libadwaita
```

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install ydotool wl-clipboard playerctl python3-evdev python3-gi gir1.2-gtk-4.0 gir1.2-adw-1
```

#### Arch Linux

```bash
sudo pacman -S ydotool wl-clipboard playerctl python-evdev python-gobject gtk4 libadwaita
```

### 3. Create Python Virtual Environment

```bash
python3.12 -m venv ~/.local/share/whisper-dictation
~/.local/share/whisper-dictation/bin/pip install --upgrade pip
~/.local/share/whisper-dictation/bin/pip install -r requirements.txt
```

This will install `nemo_toolkit[asr]` which includes:
- PyTorch with CUDA support
- NVIDIA NeMo framework
- All required dependencies

**Optional**: Install noise reduction support:

```bash
~/.local/share/whisper-dictation/bin/pip install noisereduce soundfile numpy
```

### 4. Install Scripts

```bash
mkdir -p ~/.local/bin
cp scripts/* ~/.local/bin/
chmod +x ~/.local/bin/whisper-*
chmod +x ~/.local/bin/whisperstats
```

### 5. Install Systemd Services

```bash
mkdir -p ~/.config/systemd/user

# Install daemon service
sed "s|\$HOME|$HOME|g" systemd/whisper-daemon.service.template > ~/.config/systemd/user/whisper-daemon.service

# Install hotkey service
sed "s|\$HOME|$HOME|g" systemd/whisper-hotkey.service.template > ~/.config/systemd/user/whisper-hotkey.service

# Install ydotoold service
cp systemd/ydotoold.service ~/.config/systemd/user/ydotoold.service
```

### 6. Enable and Start Services

```bash
systemctl --user daemon-reload
systemctl --user enable --now ydotoold.service
systemctl --user enable --now whisper-daemon.service
systemctl --user enable --now whisper-hotkey.service
```

### 7. Verify Installation

```bash
# Check service status
systemctl --user status whisper-daemon
systemctl --user status whisper-hotkey
systemctl --user status ydotoold

# Check daemon status
cat /tmp/whisper-daemon.status
# Should show "ready" after model loads
```

## Post-Installation

### First Use

On first use, the daemon will download the NVIDIA Parakeet TDT model (~4-8GB). This happens automatically in the background.

Monitor the download:

```bash
journalctl --user -u whisper-daemon -f
```

### Testing

1. **Double middle-click** your mouse anywhere
2. You should hear a beep sound
3. Say "Hello world period"
4. **Double middle-click** again
5. Text should be pasted: "Hello world."

If this works, you're all set!

### Statistics Dashboard

Launch the statistics app to track your usage:

```bash
whisperstats
```

## Distribution-Specific Notes

### Fedora

- Everything should work out of the box
- SELinux may need to be configured for ydotool if you encounter permission errors

### Ubuntu

- Wayland session must be explicitly selected at login (GDM shows a gear icon)
- May need to add user to `input` group for evdev access:
  ```bash
  sudo usermod -a -G input $USER
  ```
  Log out and back in after this change

### Arch Linux

- All packages available in official repos
- Use `python-evdev` instead of `python3-evdev`
- May need to start PipeWire manually if not using a DE that starts it

## Common Installation Issues

### "nvidia-smi not found"

**Solution**: Install NVIDIA drivers

```bash
# Fedora
sudo dnf install akmod-nvidia

# Ubuntu
sudo ubuntu-drivers autoinstall

# Arch
sudo pacman -S nvidia nvidia-utils
```

### "Python 3.12 not found"

**Solution**: Install Python 3.12 from your distribution's repos or use [pyenv](https://github.com/pyenv/pyenv)

### "Permission denied" on evdev

**Solution**: Add your user to the `input` group

```bash
sudo usermod -a -G input $USER
# Log out and back in
```

### "Services fail to start"

**Solution**: Check logs for specific errors

```bash
journalctl --user -u whisper-daemon -n 50
journalctl --user -u whisper-hotkey -n 50
```

### "Model download fails"

**Solution**: Check internet connection and disk space. The model downloads from HuggingFace:

```bash
# Check disk space
df -h ~/.cache/huggingface

# Clear cache and retry
rm -rf ~/.cache/huggingface/hub/models--nvidia--parakeet*
systemctl --user restart whisper-daemon
```

## Updating

To update to a newer version:

```bash
cd whisper-dictation
git pull
./install.sh
```

The installer will detect existing installation and update only what's needed.

## Uninstalling

To completely remove whisper-dictation:

```bash
cd whisper-dictation
./uninstall.sh
```

The uninstaller will prompt you about removing:
- Statistics database
- Configuration files
- Model cache (4-8GB)

## Next Steps

- Read [CONFIGURATION.md](CONFIGURATION.md) to customize settings
- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Check [DEVELOPMENT.md](DEVELOPMENT.md) if you want to contribute
