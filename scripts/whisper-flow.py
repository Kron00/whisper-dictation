#!/usr/bin/env python3
"""
Whisper Flow - Beautiful voice dictation for Linux
A Wispr Flow-inspired dictation app with GPU-accelerated transcription
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Gdk', '4.0')

try:
    gi.require_version('Gtk4LayerShell', '1.0')
    from gi.repository import Gtk4LayerShell as LayerShell
    HAS_LAYER_SHELL = True
except:
    HAS_LAYER_SHELL = False

from gi.repository import Gtk, Adw, Gdk, GLib, Gio
import subprocess
import threading
import tempfile
import os
import sys
import re

# Flow rewrite settings
FLOW_ENABLED_FILE = "/tmp/whisper-flow.enabled"
FLOW_MODE_FILE = "/tmp/whisper-flow.mode"

def is_flow_enabled():
    return os.path.exists(FLOW_ENABLED_FILE)

def flow_rewrite_regex(text):
    """Remove filler words and repeated words from transcription."""
    if not text or len(text) < 3:
        return text

    # Remove filler words
    clean = re.sub(r'\b[Uu][mh]\b', '', text)
    clean = re.sub(r'\b[Uu]hh*\b', '', clean)
    clean = re.sub(r'\b[Ee]rr*\b', '', clean)
    clean = re.sub(r'\b[Aa]hh*\b', '', clean)
    clean = re.sub(r'\b[Hh]mm+\b', '', clean)
    clean = re.sub(r'\b[Ee]rm\b', '', clean)
    clean = re.sub(r'  +', ' ', clean).strip()

    # Remove repeated words (e.g., "so so so" -> "so", "like, like, like" -> "like")
    clean = re.sub(r'\b([a-zA-Z]+)([ ,]+\1)+\b', r'\1', clean, flags=re.IGNORECASE)

    # Capitalize first letter
    if clean:
        clean = clean[0].upper() + clean[1:]

    # Add period if no ending punctuation
    if clean and clean[-1] not in '.!?':
        clean = clean + '.'

    return clean

class WhisperFlow(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.local.whisperflow',
                        flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.recording = False
        self.record_process = None
        self.audio_file = None
        self.window = None
        self.dot_bright = True
        self.model = None
        self.venv_path = os.path.expanduser("~/.local/share/whisper-dictation")

    def do_activate(self):
        self.window = RecordingOverlay(application=self)
        self.window.present()

        # Start recording immediately
        self.start_recording()

    def start_recording(self):
        self.recording = True
        self.audio_file = tempfile.mktemp(suffix='.wav')

        self.record_process = subprocess.Popen([
            'pw-record',
            '--target=@DEFAULT_AUDIO_SOURCE@',
            '--format=s16',
            '--rate=16000',
            '--channels=1',
            self.audio_file
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        self.window.set_mode('recording')

    def stop_recording(self):
        if self.record_process:
            self.record_process.terminate()
            self.record_process.wait()
            self.record_process = None

        self.recording = False
        self.window.set_mode('transcribing')

        # Transcribe in background
        thread = threading.Thread(target=self.transcribe)
        thread.daemon = True
        thread.start()

    def transcribe(self):
        try:
            # Run transcription - pass audio path as argument to avoid code injection
            result = subprocess.run([
                f'{self.venv_path}/bin/python3.12',
                '-c',
                '''
import os
import sys
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
from faster_whisper import WhisperModel
model = WhisperModel("distil-large-v3", device="cuda", compute_type="float16")
segments, _ = model.transcribe(
    sys.argv[1],
    language="en",
    beam_size=5,
    vad_filter=True,
    vad_parameters=dict(min_silence_duration_ms=250),
)
text = " ".join([s.text for s in segments]).strip()
print(text)
''',
                self.audio_file
            ], capture_output=True, text=True, timeout=60)

            text = result.stdout.strip()

            if text:
                # Apply flow rewrite if enabled
                if is_flow_enabled():
                    text = flow_rewrite_regex(text)

                # Copy to clipboard and paste
                subprocess.run(['wl-copy', text], check=True)
                ydotool_env = os.environ.copy()
                ydotool_env['YDOTOOL_SOCKET'] = f"/run/user/{os.getuid()}/ydotool.socket"
                subprocess.run(['ydotool', 'key', '29:1', '42:1', '47:1', '47:0', '42:0', '29:0'], env=ydotool_env)


            # Clean up
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)

            GLib.idle_add(self.quit)

        except Exception as e:
            print(f"Transcription error: {e}", file=sys.stderr)
            # Clean up audio file on error too
            if self.audio_file and os.path.exists(self.audio_file):
                os.remove(self.audio_file)
            GLib.idle_add(self.quit)

    def toggle(self):
        if self.recording:
            self.stop_recording()
        else:
            self.quit()


class RecordingOverlay(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_decorated(False)
        self.set_resizable(False)
        self.set_default_size(180, 48)

        # Layer shell for positioning
        if HAS_LAYER_SHELL:
            LayerShell.init_for_window(self)
            LayerShell.set_layer(self, LayerShell.Layer.OVERLAY)
            LayerShell.set_anchor(self, LayerShell.Edge.BOTTOM, True)
            LayerShell.set_anchor(self, LayerShell.Edge.LEFT, True)
            LayerShell.set_margin(self, LayerShell.Edge.BOTTOM, 40)
            LayerShell.set_margin(self, LayerShell.Edge.LEFT, 40)
            LayerShell.set_keyboard_mode(self, LayerShell.KeyboardMode.NONE)

        # Main container with styling
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.main_box.set_margin_start(16)
        self.main_box.set_margin_end(20)
        self.main_box.set_margin_top(12)
        self.main_box.set_margin_bottom(12)
        self.main_box.set_halign(Gtk.Align.CENTER)
        self.main_box.set_valign(Gtk.Align.CENTER)

        # Recording indicator dot
        self.dot = Gtk.Label(label="●")
        self.dot.add_css_class("recording-dot")
        self.main_box.append(self.dot)

        # Status label
        self.status_label = Gtk.Label(label="Recording...")
        self.status_label.add_css_class("status-label")
        self.main_box.append(self.status_label)

        self.set_content(self.main_box)

        # Apply CSS
        self.apply_styles()

        # Pulse animation
        self.pulse_bright = True
        GLib.timeout_add(400, self.pulse_dot)

        # Click to stop
        click = Gtk.GestureClick()
        click.connect('pressed', self.on_click)
        self.add_controller(click)

    def apply_styles(self):
        css = b"""
        window {
            background: alpha(#1a1a1a, 0.92);
            border-radius: 24px;
            border: 1px solid alpha(white, 0.08);
            box-shadow: 0 8px 32px alpha(black, 0.4);
        }

        .recording-dot {
            font-size: 22px;
            color: #ef4444;
            min-width: 22px;
        }

        .recording-dot.dim {
            opacity: 0.35;
        }

        .recording-dot.transcribing {
            color: #3b82f6;
        }

        .status-label {
            font-size: 14px;
            font-weight: 500;
            color: alpha(white, 0.92);
            letter-spacing: 0.3px;
        }
        """

        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def set_mode(self, mode):
        if mode == 'recording':
            self.status_label.set_text("Recording...")
            self.dot.remove_css_class("transcribing")
        elif mode == 'transcribing':
            self.status_label.set_text("Transcribing...")
            self.dot.add_css_class("transcribing")

    def pulse_dot(self):
        self.pulse_bright = not self.pulse_bright
        if self.pulse_bright:
            self.dot.remove_css_class("dim")
        else:
            self.dot.add_css_class("dim")
        return True

    def on_click(self, gesture, n_press, x, y):
        app = self.get_application()
        if app:
            app.toggle()


def main():
    app = WhisperFlow()
    return app.run(sys.argv)


if __name__ == '__main__':
    sys.exit(main())
