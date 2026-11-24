//! PCM and WAV helpers for the verification-engineering course.
//!
//! The interesting properties are ordinary audio facts: a round trip stays a
//! round trip, a hot gain clamps instead of wrapping, silence stays finite,
//! and a mix of two full-scale signals cannot exceed full scale.

mod audio;
mod error;
mod png;
mod wav;

pub use audio::{
    apply_gain_db, ensure_finite, mix, normalize_peak, peak, resample_linear, rms, AudioBuffer,
};
pub use error::{Error, Result};
pub use png::{render_waveform_png, write_waveform_png};
pub use wav::{encode_wav, parse_wav, read_wav, write_wav, SampleFormat};
