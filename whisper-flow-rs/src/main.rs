use std::cell::RefCell;
use std::f64::consts::PI;
use std::fs;
use std::io::{Read, Seek, SeekFrom};
use std::path::Path;
use std::rc::Rc;

use gtk4::cairo;
use gtk4::gdk::Display;
use gtk4::gio::ApplicationFlags;
use gtk4::glib;
use gtk4::glib::timeout_add_local;
use gtk4::prelude::*;
use gtk4::{CssProvider, DrawingArea};
use gtk4_layer_shell::{Edge, KeyboardMode, Layer, LayerShell};
use libadwaita as adw;
use libadwaita::prelude::*;

const AUDIO_FILE: &str = "/tmp/whisper-dictate.wav";
const STATE_FILE: &str = "/tmp/whisper-dictate.state";

const NUM_BARS: usize = 12;
const BAR_WIDTH: f64 = 3.0;
const BAR_GAP: f64 = 3.0;
const BAR_RADIUS: f64 = 1.5;
const MIN_BAR_HEIGHT: f64 = 3.0;
const MAX_BAR_HEIGHT: f64 = 20.0;
const PADDING_H: f64 = 10.0;
const PADDING_V: f64 = 6.0;
const PILL_WIDTH: f64 = NUM_BARS as f64 * (BAR_WIDTH + BAR_GAP) - BAR_GAP + PADDING_H * 2.0;
const PILL_HEIGHT: f64 = MAX_BAR_HEIGHT + PADDING_V * 2.0 + 4.0;
const SMOOTHING_FACTOR: f64 = 0.3;

#[derive(Clone, Copy, PartialEq)]
enum Mode {
    Recording,
    Transcribing,
}

struct OverlayState {
    mode: Mode,
    visible: bool,
    bar_heights: [f64; NUM_BARS],
    target_heights: [f64; NUM_BARS],
    idle_phase: f64,
    audio_buf: Vec<u8>,
}

impl OverlayState {
    fn new() -> Self {
        Self {
            mode: Mode::Recording,
            visible: false,
            bar_heights: [MIN_BAR_HEIGHT; NUM_BARS],
            target_heights: [MIN_BAR_HEIGHT; NUM_BARS],
            idle_phase: 0.0,
            audio_buf: vec![0u8; 3200],
        }
    }
}

fn rounded_rect(cr: &cairo::Context, x: f64, y: f64, w: f64, h: f64, r: f64) {
    let r = r.min(w / 2.0).min(h / 2.0);
    cr.new_path();
    cr.arc(x + w - r, y + r, r, -PI / 2.0, 0.0);
    cr.arc(x + w - r, y + h - r, r, 0.0, PI / 2.0);
    cr.arc(x + r, y + h - r, r, PI / 2.0, PI);
    cr.arc(x + r, y + r, r, PI, 3.0 * PI / 2.0);
    cr.close_path();
}

fn main() {
    let app = adw::Application::new(
        Some("com.local.whisperflow"),
        ApplicationFlags::NON_UNIQUE,
    );

    let state = Rc::new(RefCell::new(OverlayState::new()));

    app.connect_activate(move |app| {
        let window = adw::ApplicationWindow::new(app);
        window.set_decorated(false);
        window.set_resizable(false);

        // Layer shell setup (Niri)
        window.init_layer_shell();
        window.set_layer(Layer::Overlay);
        window.set_anchor(Edge::Bottom, true);
        window.set_margin(Edge::Bottom, 10);
        window.set_keyboard_mode(KeyboardMode::None);
        window.set_default_size(PILL_WIDTH as i32, PILL_HEIGHT as i32);

        // Drawing area
        let drawing_area = DrawingArea::new();
        drawing_area.set_content_width(PILL_WIDTH as i32);
        drawing_area.set_content_height(PILL_HEIGHT as i32);

        let draw_state = state.clone();
        drawing_area.set_draw_func(move |_area, cr, width, height| {
            let s = draw_state.borrow();
            let width = width as f64;
            let height = height as f64;

            // Clear to transparent
            cr.set_operator(cairo::Operator::Source);
            cr.set_source_rgba(0.0, 0.0, 0.0, 0.0);
            let _ = cr.paint();
            cr.set_operator(cairo::Operator::Over);

            // Pill position: centered horizontally, anchored to bottom
            let px = (width - PILL_WIDTH) / 2.0;
            let py = height - PILL_HEIGHT;

            // Pill background
            rounded_rect(cr, px, py, PILL_WIDTH, PILL_HEIGHT, PILL_HEIGHT / 2.0);
            cr.set_source_rgba(0.102, 0.102, 0.102, 0.95);
            let _ = cr.fill();

            // Bar color
            if s.mode == Mode::Recording {
                cr.set_source_rgba(1.0, 1.0, 1.0, 0.9);
            } else {
                cr.set_source_rgba(0.231, 0.510, 0.965, 0.9);
            }

            // Draw bars relative to pill position
            let center_y = py + PILL_HEIGHT / 2.0;
            let total_w = NUM_BARS as f64 * (BAR_WIDTH + BAR_GAP) - BAR_GAP;
            let start_x = px + (PILL_WIDTH - total_w) / 2.0;

            for i in 0..NUM_BARS {
                let x = start_x + i as f64 * (BAR_WIDTH + BAR_GAP);
                let h = s.bar_heights[i];
                let y = center_y - h / 2.0;
                rounded_rect(cr, x, y, BAR_WIDTH, h, BAR_RADIUS);
                let _ = cr.fill();
            }
        });

        window.set_content(Some(&drawing_area));

        // CSS for transparent background (must override Adwaita's window.background)
        let css = CssProvider::new();
        css.load_from_data(
            "window, window.background, .background { background: transparent; background-color: transparent; } \
             window > *, .background > * { background: transparent; }",
        );
        gtk4::style_context_add_provider_for_display(
            &Display::default().unwrap(),
            &css,
            gtk4::STYLE_PROVIDER_PRIORITY_APPLICATION + 1,
        );

        // Check initial state
        let mut s = state.borrow_mut();
        if Path::new(STATE_FILE).exists() {
            s.mode = Mode::Recording;
            s.visible = true;
            drop(s);
            window.present();
        } else {
            s.visible = false;
            drop(s);
            window.set_visible(false);
        }

        // Animation timer (16ms ~60fps)
        let anim_state = state.clone();
        let anim_da = drawing_area.clone();
        timeout_add_local(std::time::Duration::from_millis(16), move || {
            let mut s = anim_state.borrow_mut();
            if !s.visible {
                return glib::ControlFlow::Continue;
            }

            let mut changed = false;
            for i in 0..NUM_BARS {
                let diff = s.target_heights[i] - s.bar_heights[i];
                if diff.abs() > 0.3 {
                    s.bar_heights[i] += diff * SMOOTHING_FACTOR;
                    changed = true;
                } else {
                    s.bar_heights[i] = s.target_heights[i];
                }
            }

            if s.mode == Mode::Transcribing {
                // Idle sine wave animation
                s.idle_phase += 0.06;
                for i in 0..NUM_BARS {
                    let wave = (s.idle_phase + i as f64 * 0.45).sin() * 0.5 + 0.5;
                    s.target_heights[i] =
                        MIN_BAR_HEIGHT + wave * (MAX_BAR_HEIGHT * 0.35 - MIN_BAR_HEIGHT);
                }
                drop(s);
                anim_da.queue_draw();
            } else if changed {
                drop(s);
                anim_da.queue_draw();
            }

            glib::ControlFlow::Continue
        });

        // Audio read timer (50ms)
        let audio_state = state.clone();
        timeout_add_local(std::time::Duration::from_millis(50), move || {
            let mut s = audio_state.borrow_mut();
            if !s.visible || s.mode != Mode::Recording {
                return glib::ControlFlow::Continue;
            }

            let path = Path::new(AUDIO_FILE);
            if !path.exists() {
                return glib::ControlFlow::Continue;
            }

            let file_size = match fs::metadata(path) {
                Ok(m) => m.len(),
                Err(_) => return glib::ControlFlow::Continue,
            };

            if file_size < 48 {
                return glib::ControlFlow::Continue;
            }

            let bytes_needed: u64 = 3200;
            let read_start = 44u64.max(file_size - bytes_needed);

            if let Ok(mut f) = fs::File::open(path) {
                if f.seek(SeekFrom::Start(read_start)).is_ok() {
                    let to_read = (file_size - read_start) as usize;
                    let to_read = to_read.min(s.audio_buf.len());
                    if let Ok(n) = f.read(&mut s.audio_buf[..to_read]) {
                        if n >= 4 {
                            let num_samples = n / 2;
                            let seg_size = (num_samples / NUM_BARS).max(1);

                            for i in 0..NUM_BARS {
                                let start = i * seg_size;
                                let end = ((i + 1) * seg_size).min(num_samples);
                                if start >= num_samples {
                                    s.target_heights[i] = MIN_BAR_HEIGHT;
                                    continue;
                                }

                                let mut sum_sq: f64 = 0.0;
                                let count = end - start;
                                for j in start..end {
                                    let byte_idx = j * 2;
                                    if byte_idx + 1 < n {
                                        let sample = i16::from_le_bytes([
                                            s.audio_buf[byte_idx],
                                            s.audio_buf[byte_idx + 1],
                                        ]) as f64;
                                        sum_sq += sample * sample;
                                    }
                                }

                                let rms = (sum_sq / count as f64).sqrt();
                                let normalized = (rms / 3000.0).min(1.0).sqrt();
                                s.target_heights[i] = MIN_BAR_HEIGHT
                                    + normalized * (MAX_BAR_HEIGHT - MIN_BAR_HEIGHT);
                            }
                        }
                    }
                }
            }

            glib::ControlFlow::Continue
        });

        // State file check timer (150ms)
        let state_check = state.clone();
        let win_ref = window.clone();
        timeout_add_local(std::time::Duration::from_millis(150), move || {
            let mut s = state_check.borrow_mut();

            if Path::new(STATE_FILE).exists() {
                if let Ok(content) = fs::read_to_string(STATE_FILE) {
                    let trimmed = content.trim();
                    if trimmed == "transcribing" {
                        s.mode = Mode::Transcribing;
                    } else if trimmed == "recording" {
                        s.mode = Mode::Recording;
                    }
                }
                if !s.visible {
                    s.visible = true;
                    s.bar_heights = [MIN_BAR_HEIGHT; NUM_BARS];
                    s.target_heights = [MIN_BAR_HEIGHT; NUM_BARS];
                    drop(s);
                    win_ref.present();
                }
            } else if s.visible {
                s.visible = false;
                drop(s);
                win_ref.set_visible(false);
            }

            glib::ControlFlow::Continue
        });
    });

    app.run();
}
