#!/usr/bin/env bash
set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
echo_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
echo_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Pre-flight checks
check_gpu() {
    echo_info "Checking GPU..."
    if ! command -v nvidia-smi &>/dev/null; then
        echo_error "nvidia-smi not found - NVIDIA drivers not installed"
        echo_error "Please install NVIDIA drivers and CUDA before continuing"
        return 1
    fi

    # Check for at least 3GB VRAM
    vram=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
    if (( vram < 3000 )); then
        echo_error "Insufficient VRAM: ${vram}MB (need 3GB+ recommended)"
        echo_warn "Installation will continue but performance may be degraded"
    fi

    gpu_name=$(nvidia-smi --query-gpu=name --format=csv,noheader | head -1)
    echo_info "GPU OK: ${gpu_name} (${vram}MB VRAM)"
}

check_python() {
    echo_info "Checking Python 3.12..."
    if ! command -v python3.12 &>/dev/null; then
        echo_error "Python 3.12 not found"
        echo_error "Please install Python 3.12 before continuing"
        return 1
    fi
    echo_info "Python 3.12 OK"
}

check_distro() {
    if command -v dnf &>/dev/null; then
        DISTRO="fedora"
        echo_info "Detected: Fedora/RHEL"
    elif command -v apt &>/dev/null; then
        DISTRO="ubuntu"
        echo_info "Detected: Ubuntu/Debian"
    elif command -v pacman &>/dev/null; then
        DISTRO="arch"
        echo_info "Detected: Arch Linux"
    else
        DISTRO="unknown"
        echo_warn "Unknown distribution - you'll need to install dependencies manually"
    fi
}

# Install system dependencies
install_system_deps() {
    echo_info "Installing system dependencies..."

    case "$DISTRO" in
        fedora)
            sudo dnf install -y ydotool wl-clipboard playerctl python3-evdev python3-gobject gtk4 libadwaita
            ;;
        ubuntu)
            sudo apt update
            sudo apt install -y ydotool wl-clipboard playerctl python3-evdev python3-gi gir1.2-gtk-4.0 gir1.2-adw-1
            ;;
        arch)
            sudo pacman -S --needed ydotool wl-clipboard playerctl python-evdev python-gobject gtk4 libadwaita
            ;;
        *)
            echo_error "Please install these packages manually:"
            echo "  - ydotool"
            echo "  - wl-clipboard"
            echo "  - playerctl"
            echo "  - python3-evdev"
            echo "  - python3-gobject / python-gobject"
            echo "  - gtk4"
            echo "  - libadwaita"
            read -p "Press Enter when done, or Ctrl+C to exit..."
            ;;
    esac

    echo_info "System dependencies installed"
}

# Create Python virtual environment
setup_venv() {
    VENV_PATH="$HOME/.local/share/whisper-dictation"
    echo_info "Creating Python virtual environment at $VENV_PATH"

    if [[ -d "$VENV_PATH" ]]; then
        echo_warn "Virtual environment already exists at $VENV_PATH"
        read -p "Remove and recreate? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_PATH"
        else
            echo_info "Skipping venv creation"
            return 0
        fi
    fi

    python3.12 -m venv "$VENV_PATH"

    echo_info "Installing Python packages (this may take 5-10 minutes)..."
    "$VENV_PATH/bin/pip" install --upgrade pip
    "$VENV_PATH/bin/pip" install -r requirements.txt

    # Optional: noise reduction packages
    read -p "Install optional noise reduction support? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        "$VENV_PATH/bin/pip" install noisereduce soundfile numpy
        echo_info "Noise reduction support installed"
    fi

    echo_info "Python environment ready"
}

# Install scripts
install_scripts() {
    echo_info "Installing scripts to ~/.local/bin/"
    mkdir -p "$HOME/.local/bin"

    cp scripts/* "$HOME/.local/bin/"
    chmod +x "$HOME/.local/bin"/whisper-*
    chmod +x "$HOME/.local/bin/whisperstats"

    echo_info "Scripts installed successfully"
}

# Install systemd services
install_services() {
    echo_info "Installing systemd user services"
    mkdir -p "$HOME/.config/systemd/user"

    # Substitute $HOME in templates
    sed "s|\$HOME|$HOME|g" systemd/whisper-daemon.service.template > "$HOME/.config/systemd/user/whisper-daemon.service"
    sed "s|\$HOME|$HOME|g" systemd/whisper-hotkey.service.template > "$HOME/.config/systemd/user/whisper-hotkey.service"
    cp systemd/ydotoold.service "$HOME/.config/systemd/user/ydotoold.service"

    systemctl --user daemon-reload

    # Enable services
    systemctl --user enable ydotoold.service
    systemctl --user enable whisper-daemon.service
    systemctl --user enable whisper-hotkey.service

    # Start services
    echo_info "Starting services..."
    systemctl --user start ydotoold.service
    systemctl --user start whisper-daemon.service
    systemctl --user start whisper-hotkey.service

    echo_info "Services installed and started"
}

# Download model (optional)
download_model() {
    read -p "Pre-download Parakeet model now? (4-8GB download) (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo_info "Model will download automatically on first use via daemon"
        echo_info "Monitor progress: journalctl --user -u whisper-daemon -f"
    fi
}

# Validation
validate_installation() {
    echo_info "Validating installation..."

    # Check if services are running
    sleep 2  # Give services time to start

    if systemctl --user is-active --quiet whisper-daemon.service; then
        echo_info "✓ whisper-daemon is running"
    else
        echo_warn "✗ whisper-daemon not running - check: journalctl --user -u whisper-daemon"
    fi

    if systemctl --user is-active --quiet whisper-hotkey.service; then
        echo_info "✓ whisper-hotkey is running"
    else
        echo_warn "✗ whisper-hotkey not running - check: journalctl --user -u whisper-hotkey"
    fi

    if systemctl --user is-active --quiet ydotoold.service; then
        echo_info "✓ ydotoold is running"
    else
        echo_warn "✗ ydotoold not running - check: journalctl --user -u ydotoold"
    fi

    # Check daemon status file
    sleep 3  # Give daemon time to initialize
    if [[ -f /tmp/whisper-daemon.status ]]; then
        status=$(cat /tmp/whisper-daemon.status)
        case "$status" in
            ready) echo_info "✓ Daemon ready for transcription" ;;
            starting) echo_warn "⏳ Daemon still starting (model downloading)..." ;;
            error:*) echo_error "✗ Daemon error: ${status#error: }" ;;
        esac
    else
        echo_warn "⏳ Daemon status file not yet created"
    fi
}

# Main installation flow
main() {
    echo ""
    echo "=========================================="
    echo "  Whisper Dictation Installation"
    echo "=========================================="
    echo ""

    check_gpu || exit 1
    check_python || exit 1
    check_distro

    echo ""
    echo_info "Starting installation..."
    echo ""

    install_system_deps
    setup_venv
    install_scripts
    install_services
    download_model
    validate_installation

    echo ""
    echo "=========================================="
    echo_info "Installation complete!"
    echo "=========================================="
    echo ""
    echo "Usage:"
    echo "  - Double middle-click to start/stop recording"
    echo "  - Speak with punctuation commands (see README.md)"
    echo "  - Run 'whisperstats' to view statistics"
    echo ""
    echo "Troubleshooting:"
    echo "  - Check daemon logs: journalctl --user -u whisper-daemon -f"
    echo "  - Check hotkey logs: journalctl --user -u whisper-hotkey -f"
    echo "  - See docs/TROUBLESHOOTING.md for common issues"
    echo ""
    echo "The Parakeet model (4-8GB) will download on first use."
    echo "Monitor: journalctl --user -u whisper-daemon -f"
    echo ""
}

main "$@"
