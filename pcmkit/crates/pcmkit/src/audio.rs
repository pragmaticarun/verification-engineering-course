use crate::error::{Error, Result};

/// Interleaved PCM in floating point, nominal range `[-1, 1]`.
#[derive(Clone, Debug, PartialEq)]
pub struct AudioBuffer {
    pub sample_rate: u32,
    pub channels: u16,
    pub samples: Vec<f32>,
}

impl AudioBuffer {
    pub fn new(sample_rate: u32, channels: u16, samples: Vec<f32>) -> Result<Self> {
        if sample_rate == 0 {
            return Err(Error::Audio("sample rate must be greater than zero".into()));
        }
        if channels == 0 {
            return Err(Error::Audio(
                "channel count must be greater than zero".into(),
            ));
        }
        if samples.len() % channels as usize != 0 {
            return Err(Error::Audio(
                "sample count is not a multiple of the channel count".into(),
            ));
        }
        ensure_finite(&samples)?;
        Ok(Self {
            sample_rate,
            channels,
            samples,
        })
    }

    pub fn frames(&self) -> usize {
        self.samples.len() / self.channels as usize
    }
}

pub fn ensure_finite(samples: &[f32]) -> Result<()> {
    if samples.iter().any(|s| !s.is_finite()) {
        return Err(Error::Audio(
            "non-finite sample (NaN or infinity) is not audio".into(),
        ));
    }
    Ok(())
}

/// Multiply by `10^(db/20)` and clamp to `[-1, 1]`.
///
/// The input is checked before any sample is written, so a bad buffer is left unchanged.
pub fn apply_gain_db(samples: &mut [f32], db: f32) -> Result<()> {
    ensure_finite(samples)?;
    if !db.is_finite() {
        return Err(Error::Audio("gain in dB must be finite".into()));
    }
    let factor = 10f32.powf(db / 20.0);
    if !factor.is_finite() {
        return Err(Error::Audio("gain factor overflowed".into()));
    }
    for sample in samples.iter_mut() {
        *sample = (*sample * factor).clamp(-1.0, 1.0);
    }
    Ok(())
}

/// Scale so the peak magnitude is 1. Exact silence stays silence.
pub fn normalize_peak(samples: &mut [f32]) -> Result<()> {
    ensure_finite(samples)?;
    let peak = samples.iter().fold(0.0f32, |acc, s| acc.max(s.abs()));
    if peak == 0.0 {
        return Ok(());
    }
    let factor = 1.0 / peak;
    for sample in samples.iter_mut() {
        *sample = (*sample * factor).clamp(-1.0, 1.0);
    }
    Ok(())
}

pub fn peak(samples: &[f32]) -> Result<f32> {
    ensure_finite(samples)?;
    Ok(samples.iter().fold(0.0f32, |acc, s| acc.max(s.abs())))
}

pub fn rms(samples: &[f32]) -> Result<f32> {
    ensure_finite(samples)?;
    if samples.is_empty() {
        return Ok(0.0);
    }
    let sum_sq: f32 = samples.iter().map(|s| s * s).sum();
    Ok((sum_sq / samples.len() as f32).sqrt())
}

/// Sample-wise sum. Rates, channel counts, and lengths must match. The sum is clamped.
pub fn mix(a: &AudioBuffer, b: &AudioBuffer) -> Result<AudioBuffer> {
    if a.sample_rate != b.sample_rate {
        return Err(Error::Audio(
            "cannot mix buffers with different sample rates".into(),
        ));
    }
    if a.channels != b.channels {
        return Err(Error::Audio(
            "cannot mix buffers with different channel counts".into(),
        ));
    }
    if a.samples.len() != b.samples.len() {
        return Err(Error::Audio(
            "cannot mix buffers with different lengths".into(),
        ));
    }
    let mut samples = Vec::with_capacity(a.samples.len());
    for (left, right) in a.samples.iter().zip(b.samples.iter()) {
        samples.push((*left + *right).clamp(-1.0, 1.0));
    }
    AudioBuffer::new(a.sample_rate, a.channels, samples)
}

/// Linear interpolation. Endpoints are preserved when both lengths are at least one frame.
pub fn resample_linear(audio: &AudioBuffer, new_rate: u32) -> Result<AudioBuffer> {
    if new_rate == 0 {
        return Err(Error::Audio(
            "new sample rate must be greater than zero".into(),
        ));
    }
    ensure_finite(&audio.samples)?;
    if new_rate == audio.sample_rate || audio.frames() == 0 {
        return AudioBuffer::new(new_rate, audio.channels, audio.samples.clone());
    }
    let channels = audio.channels as usize;
    let in_frames = audio.frames();
    let out_frames = usize::try_from(
        (in_frames as u128 * u128::from(new_rate) + u128::from(audio.sample_rate) / 2)
            / u128::from(audio.sample_rate),
    )
    .unwrap_or(usize::MAX);
    let out_frames = out_frames.max(1);
    let mut samples = vec![0.0f32; out_frames * channels];
    for frame in 0..out_frames {
        let position = if out_frames == 1 {
            0.0
        } else {
            frame as f32 * (in_frames - 1) as f32 / (out_frames - 1) as f32
        };
        let left = (position.floor() as usize).min(in_frames - 1);
        let right = (left + 1).min(in_frames - 1);
        let frac = position - left as f32;
        for ch in 0..channels {
            let a = audio.samples[left * channels + ch];
            let b = audio.samples[right * channels + ch];
            samples[frame * channels + ch] = a + (b - a) * frac;
        }
    }
    AudioBuffer::new(new_rate, audio.channels, samples)
}

#[cfg(test)]
mod tests {
    use super::*;

    fn buf(samples: Vec<f32>) -> AudioBuffer {
        AudioBuffer::new(8_000, 1, samples).unwrap()
    }

    #[test]
    fn zero_db_is_identity_inside_full_scale() {
        let mut samples = vec![0.25, -0.5, 0.0, 1.0, -1.0];
        let original = samples.clone();
        apply_gain_db(&mut samples, 0.0).unwrap();
        for (got, want) in samples.iter().zip(original) {
            assert!((got - want).abs() < 1e-6);
        }
    }

    #[test]
    fn hot_gain_clamps_instead_of_wrapping() {
        let mut samples = vec![0.5, -0.2];
        apply_gain_db(&mut samples, 60.0).unwrap();
        assert!((samples[0] - 1.0).abs() < 1e-6);
        assert!((samples[1] + 1.0).abs() < 1e-6);
    }

    #[test]
    fn non_finite_input_is_rejected_without_writing() {
        let mut samples = vec![0.2, f32::NAN];
        let err = apply_gain_db(&mut samples, 6.0).unwrap_err();
        assert!(err.to_string().contains("non-finite"));
        assert!(samples[1].is_nan());
        assert!((samples[0] - 0.2).abs() < 1e-6);
    }

    #[test]
    fn normalize_lifts_peak_and_leaves_silence_alone() {
        let mut quiet = vec![0.0, 0.0];
        normalize_peak(&mut quiet).unwrap();
        assert_eq!(quiet, vec![0.0, 0.0]);
        let mut hot = vec![0.25, -0.5];
        normalize_peak(&mut hot).unwrap();
        let p = peak(&hot).unwrap();
        assert!((p - 1.0).abs() < 1e-5);
        assert!(hot
            .iter()
            .all(|s| s.is_finite() && (-1.0..=1.0).contains(s)));
    }

    #[test]
    fn negative_gain_never_increases_peak_on_full_scale_audio() {
        let mut state: u32 = 0x1234_5678;
        for _ in 0..80 {
            state = state.wrapping_mul(1_664_525).wrapping_add(1_013_904_223);
            let n = 1 + (state % 16) as usize;
            let mut samples = Vec::with_capacity(n);
            for _ in 0..n {
                state = state.wrapping_mul(1_664_525).wrapping_add(1_013_904_223);
                let unit = (state % 2_001) as f32 / 1_000.0 - 1.0;
                samples.push(unit);
            }
            state = state.wrapping_mul(1_664_525).wrapping_add(1_013_904_223);
            let db = -((state % 2_401) as f32) / 100.0;
            let before = peak(&samples).unwrap();
            apply_gain_db(&mut samples, db).unwrap();
            let after = peak(&samples).unwrap();
            assert!(
                after <= before + 1e-5,
                "negative gain {db} dB raised peak from {before} to {after}"
            );
            assert!(samples
                .iter()
                .all(|s| s.is_finite() && (-1.0..=1.0).contains(s)));
        }
    }

    #[test]
    fn mix_clamps_and_rejects_a_shape_mismatch() {
        let mixed = mix(&buf(vec![0.75, -0.25]), &buf(vec![0.75, -0.25])).unwrap();
        assert!((mixed.samples[0] - 1.0).abs() < 1e-6);
        assert!((mixed.samples[1] + 0.5).abs() < 1e-6);
        let other = AudioBuffer::new(16_000, 1, vec![0.1, 0.1]).unwrap();
        assert!(mix(&buf(vec![0.1, 0.1]), &other).is_err());
    }

    #[test]
    fn resample_preserves_endpoints() {
        let audio = buf(vec![0.0, 0.5, 1.0, 0.25]);
        let out = resample_linear(&audio, 16_000).unwrap();
        assert_eq!(out.sample_rate, 16_000);
        assert!(out.frames() > audio.frames());
        assert!(out.samples[0].abs() < 1e-6);
        assert!((out.samples[out.samples.len() - 1] - 0.25).abs() < 1e-5);
        assert!(out.samples.iter().all(|s| s.is_finite()));
    }

    #[test]
    fn rms_of_a_constant_is_its_magnitude() {
        let value = rms(&[0.5, -0.5, 0.5, -0.5]).unwrap();
        assert!((value - 0.5).abs() < 1e-6);
    }
}
