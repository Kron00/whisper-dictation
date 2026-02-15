#!/usr/bin/env python3
"""
Whisper Flow - Animated waveform overlay for voice dictation
A pure visual indicator that stays resident for instant display.
Reads the growing WAV file for live audio levels.
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
import cairo
import struct
import math
import os
import sys

AUDIO_FILE = "/tmp/whisper-dictate.wav"
STATE_FILE = "/tmp/whisper-dictate.state"

# Waveform config
NUM_BARS = 12
BAR_WIDTH = 3
BAR_GAP = 3
BAR_RADIUS = 1.5
MIN_BAR_HEIGHT = 3
MAX_BAR_HEIGHT = 20
PADDING_H = 10
PADDING_V = 6
PILL_WIDTH = NUM_BARS * (BAR_WIDTH + BAR_GAP) - BAR_GAP + PADDING_H * 2
PILL_HEIGHT = MAX_BAR_HEIGHT + PADDING_V * 2 + 4

# Smoothing
SMOOTHING_FACTOR = 0.3


class WaveformOverlay(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_decorated(False)
        self.set_resizable(False)
        self.set_default_size(PILL_WIDTH, PILL_HEIGHT)

        if HAS_LAYER_SHELL:
            LayerShell.init_for_window(self)
            LayerShell.set_layer(self, LayerShell.Layer.OVERLAY)
            LayerShell.set_anchor(self, LayerShell.Edge.BOTTOM, True)
            LayerShell.set_margin(self, LayerShell.Edge.BOTTOM, 10)
            LayerShell.set_keyboard_mode(self, LayerShell.KeyboardMode.NONE)

        self.mode = 'recording'
        self.visible_state = False
        self.bar_heights = [MIN_BAR_HEIGHT] * NUM_BARS
        self.target_heights = [MIN_BAR_HEIGHT] * NUM_BARS
        self.idle_phase = 0.0

        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_content_width(PILL_WIDTH)
        self.drawing_area.set_content_height(PILL_HEIGHT)
        self.drawing_area.set_draw_func(self._draw)
        self.set_content(self.drawing_area)

        self._apply_styles()

        GLib.timeout_add(16, self._animate)
        GLib.timeout_add(50, self._read_audio)

    def _apply_styles(self):
        css = b"""
        window {
            background: transparent;
            min-width: 0;
            min-height: 0;
        }
        window > * {
            min-width: 0;
            min-height: 0;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION + 1
        )

    def show_overlay(self):
        if not self.visible_state:
            self.visible_state = True
            self.bar_heights = [MIN_BAR_HEIGHT] * NUM_BARS
            self.target_heights = [MIN_BAR_HEIGHT] * NUM_BARS
            self.present()

    def hide_overlay(self):
        if self.visible_state:
            self.visible_state = False
            self.set_visible(False)

    def set_mode(self, mode):
        self.mode = mode

    def _draw(self, area, cr, width, height):
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.set_source_rgba(0, 0, 0, 0)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

        pw, ph = PILL_WIDTH, PILL_HEIGHT
        px = (width - pw) / 2
        py = height - ph
        self._rounded_rect(cr, px, py, pw, ph, ph / 2)
        cr.set_source_rgba(0.102, 0.102, 0.102, 0.95)
        cr.fill()

        if self.mode == 'recording':
            cr.set_source_rgba(1.0, 1.0, 1.0, 0.9)
        else:
            cr.set_source_rgba(0.231, 0.510, 0.965, 0.9)

        center_y = height - ph / 2
        total_w = NUM_BARS * (BAR_WIDTH + BAR_GAP) - BAR_GAP
        start_x = (width - total_w) / 2

        for i in range(NUM_BARS):
            x = start_x + i * (BAR_WIDTH + BAR_GAP)
            h = self.bar_heights[i]
            y = center_y - h / 2
            self._rounded_rect(cr, x, y, BAR_WIDTH, h, BAR_RADIUS)
            cr.fill()

    def _rounded_rect(self, cr, x, y, w, h, r):
        r = min(r, w / 2, h / 2)
        cr.new_path()
        cr.arc(x + w - r, y + r, r, -math.pi / 2, 0)
        cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
        cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
        cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
        cr.close_path()

    def _animate(self):
        if not self.visible_state:
            return True

        changed = False
        for i in range(NUM_BARS):
            diff = self.target_heights[i] - self.bar_heights[i]
            if abs(diff) > 0.3:
                self.bar_heights[i] += diff * SMOOTHING_FACTOR
                changed = True
            else:
                self.bar_heights[i] = self.target_heights[i]

        if self.mode == 'transcribing':
            self._update_idle_animation()
            self.drawing_area.queue_draw()
        elif changed:
            self.drawing_area.queue_draw()
        return True

    def _update_idle_animation(self):
        self.idle_phase += 0.06
        for i in range(NUM_BARS):
            wave = math.sin(self.idle_phase + i * 0.45) * 0.5 + 0.5
            self.target_heights[i] = MIN_BAR_HEIGHT + wave * (MAX_BAR_HEIGHT * 0.35 - MIN_BAR_HEIGHT)

    def _read_audio(self):
        if not self.visible_state or self.mode != 'recording':
            return True
        try:
            if not os.path.exists(AUDIO_FILE):
                return True
            file_size = os.path.getsize(AUDIO_FILE)
            if file_size < 48:
                return True

            bytes_needed = 3200
            read_start = max(44, file_size - bytes_needed)
            with open(AUDIO_FILE, 'rb') as f:
                f.seek(read_start)
                raw = f.read(bytes_needed)
            if len(raw) < 4:
                return True

            num_samples = len(raw) // 2
            samples = struct.unpack(f'<{num_samples}h', raw[:num_samples * 2])
            seg_size = max(1, num_samples // NUM_BARS)
            for i in range(NUM_BARS):
                start = i * seg_size
                end = min(start + seg_size, num_samples)
                if start >= num_samples:
                    self.target_heights[i] = MIN_BAR_HEIGHT
                    continue
                segment = samples[start:end]
                rms = math.sqrt(sum(s * s for s in segment) / len(segment))
                normalized = min(1.0, rms / 3000) ** 0.5
                self.target_heights[i] = MIN_BAR_HEIGHT + normalized * (MAX_BAR_HEIGHT - MIN_BAR_HEIGHT)
        except Exception:
            pass
        return True


class WhisperFlowApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id='com.local.whisperflow',
                        flags=Gio.ApplicationFlags.NON_UNIQUE)
        self.window = None

    def do_activate(self):
        if not self.window:
            self.window = WaveformOverlay(application=self)

        # Check state immediately
        if os.path.exists(STATE_FILE):
            self.window.set_mode('recording')
            self.window.show_overlay()
        else:
            self.window.hide_overlay()

        GLib.timeout_add(150, self._check_state)

    def _check_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE) as f:
                    state = f.read().strip()
                if state == 'transcribing':
                    self.window.set_mode('transcribing')
                elif state == 'recording':
                    self.window.set_mode('recording')
                self.window.show_overlay()
            except Exception:
                pass
        else:
            self.window.hide_overlay()
        return True


def main():
    app = WhisperFlowApp()
    return app.run(sys.argv)


if __name__ == '__main__':
    sys.exit(main())
