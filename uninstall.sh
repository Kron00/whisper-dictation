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

echo ""
echo "=========================================="
echo "  Whisper Dictation Uninstall"
echo "=========================================="
echo ""

# Stop and disable services
echo_info "Stopping services..."
systemctl --user stop whisper-daemon.service 2>/dev/null || true
systemctl --user stop whisper-hotkey.service 2>/dev/null || true
systemctl --user stop ydotoold.service 2>/dev/null || true

echo_info "Disabling services..."
systemctl --user disable whisper-daemon.service 2>/dev/null || true
systemctl --user disable whisper-hotkey.service 2>/dev/null || true
systemctl --user disable ydotoold.service 2>/dev/null || true

# Remove service files
echo_info "Removing service files..."
rm -f ~/.config/systemd/user/whisper-daemon.service
rm -f ~/.config/systemd/user/whisper-hotkey.service
rm -f ~/.config/systemd/user/ydotoold.service

systemctl --user daemon-reload

# Remove scripts
echo_info "Removing scripts..."
rm -f ~/.local/bin/whisper-daemon
rm -f ~/.local/bin/whisper-dictate
rm -f ~/.local/bin/whisper-hotkey
rm -f ~/.local/bin/whisper-autogain
rm -f ~/.local/bin/whisper-mode
rm -f ~/.local/bin/whisper-stream
rm -f ~/.local/bin/whisper-flow
rm -f ~/.local/bin/whisper-flow.py
rm -f ~/.local/bin/whisper-ding
rm -f ~/.local/bin/whisper-noise
rm -f ~/.local/bin/whisperstats

# Remove virtual environment
echo_info "Removing Python virtual environment..."
rm -rf ~/.local/share/whisper-dictation/

# Remove temporary files
echo_info "Removing temporary files..."
rm -f /tmp/whisper-daemon.sock
rm -f /tmp/whisper-daemon.status
rm -f /tmp/whisper-daemon.pid
rm -f /tmp/whisper-autogain-restore
rm -f /tmp/whisper-noise-reduction.enabled

# Optional: Remove stats database
read -p "Delete statistics database? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f ~/.local/share/whisper-dictation/stats.db
    echo_info "Statistics database deleted"
fi

# Optional: Remove config
read -p "Delete configuration files? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf ~/.config/whisper-dictation/
    echo_info "Configuration deleted"
fi

# Optional: Remove model cache
read -p "Delete model cache? (4-8GB will need re-download if reinstalled) (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo_warn "Removing HuggingFace model cache (this affects ALL models, not just Whisper)..."
    read -p "Are you sure? This removes ~/.cache/huggingface/ (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf ~/.cache/huggingface/
        echo_info "Model cache deleted"
    fi
fi

echo ""
echo "=========================================="
echo_info "Uninstall complete!"
echo "=========================================="
echo ""
echo "Thank you for using Whisper Dictation!"
echo ""
