//! Properties, goldens, a parser smoke, and an exhaustive gain check.
//!
//! These run under ordinary `cargo test`. They are the fast tier's Rust
//! half. Coverage-guided fuzzing, Miri, and Kani are separate and are not
//! hidden inside this file's pass.

use crate::{
    apply_gain_db, encode_wav, normalize_peak, parse_wav, peak, render_waveform_png, AudioBuffer,
    SampleFormat,
};

fn tone() -> AudioBuffer {
    AudioBuffer::new(48_000, 1, vec![0.0, 0.5, -0.5, 1.0]).unwrap()
}

fn golden(name: &str) -> std::path::PathBuf {
    std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../golden")
        .join(name)
}

fn xorshift(state: &mut u32) -> u32 {
    *state = state.wrapping_mul(1_664_525).wrapping_add(1_013_904_223);
    *state
}

#[test]
fn golden_wav_and_png_match_committed_bytes() {
    let audio = tone();
    let wav = encode_wav(&audio, SampleFormat::I16).unwrap();
    let png = render_waveform_png(&audio, 32).unwrap();
    let wav_path = golden("tone_i16.wav");
    let png_path = golden("tone.png");
    if std::env::var_os("UPDATE_GOLDEN").is_some() {
        std::fs::write(&wav_path, &wav).unwrap();
        std::fs::write(&png_path, &png).unwrap();
    }
    assert_eq!(
        std::fs::read(&wav_path).expect("missing golden wav"),
        wav,
        "WAV golden drifted; regenerate with UPDATE_GOLDEN=1 and review the diff"
    );
    assert_eq!(
        std::fs::read(&png_path).expect("missing golden png"),
        png,
        "PNG golden drifted; regenerate with UPDATE_GOLDEN=1 and review the diff"
    );
}

#[test]
fn i16_encoding_is_idempotent_on_a_fixed_seed() {
    let mut state = 0x0A11_5EED;
    for _ in 0..48 {
        let n = 1 + (xorshift(&mut state) % 12) as usize;
        let mut samples = Vec::with_capacity(n);
        for _ in 0..n {
            let unit = (xorshift(&mut state) % 20_001) as f32 / 10_000.0 - 1.0;
            samples.push(unit);
        }
        let audio = AudioBuffer::new(16_000, 1, samples).unwrap();
        let once = encode_wav(&audio, SampleFormat::I16).unwrap();
        let back = parse_wav(&once).unwrap();
        let twice = encode_wav(&back, SampleFormat::I16).unwrap();
        assert_eq!(once, twice);
        assert!(back.samples.iter().all(|sample| sample.is_finite()));
    }
}

#[test]
fn normalize_is_idempotent_on_a_fixed_seed() {
    let mut state = 0x0A11_5EED;
    for _ in 0..48 {
        let n = 1 + (xorshift(&mut state) % 8) as usize;
        let mut samples = Vec::with_capacity(n);
        for _ in 0..n {
            let unit = (xorshift(&mut state) % 10_001) as f32 / 10_000.0;
            samples.push(unit);
        }
        if xorshift(&mut state) % 5 == 0 {
            samples = vec![0.0; n];
        }
        normalize_peak(&mut samples).unwrap();
        let once = samples.clone();
        normalize_peak(&mut samples).unwrap();
        for (left, right) in once.iter().zip(&samples) {
            assert!((left - right).abs() < 1e-6);
        }
        let p = peak(&samples).unwrap();
        if once.iter().any(|sample| *sample != 0.0) {
            assert!((p - 1.0).abs() < 1e-5);
        } else {
            assert_eq!(p, 0.0);
        }
    }
}

#[test]
fn parser_does_not_panic_on_a_fixed_fuzz_smoke() {
    let mut state = 0xF422_0001;
    let valid = encode_wav(&tone(), SampleFormat::I16).unwrap();
    for i in 0..160 {
        let mut bytes = if i % 4 == 0 {
            let mut mutated = valid.clone();
            let index = (xorshift(&mut state) as usize) % mutated.len();
            mutated[index] ^= 0xFF;
            mutated
        } else {
            let len = (xorshift(&mut state) % 96) as usize;
            let mut random = vec![0u8; len];
            for byte in &mut random {
                *byte = (xorshift(&mut state) >> 24) as u8;
            }
            random
        };
        if bytes.len() > 4 && i % 7 == 0 {
            bytes.truncate(4);
        }
        let parsed = std::panic::catch_unwind(|| parse_wav(&bytes));
        assert!(parsed.is_ok(), "parser panicked on smoke case {i}");
    }
}

#[test]
fn every_i16_code_stays_in_range_at_the_gain_grid() {
    // Exhaustive over the i16 codes at five gains. This is not a Kani proof
    // over every f32. It is the bounded check CI actually runs.
    for code in i16::MIN..=i16::MAX {
        let sample = f32::from(code) / 32_768.0;
        for db in [-120.0_f32, -6.0, 0.0, 6.0, 60.0] {
            let mut buffer = [sample];
            apply_gain_db(&mut buffer, db).unwrap();
            assert!(
                buffer[0].is_finite() && (-1.0..=1.0).contains(&buffer[0]),
                "code {code} at {db} dB left the range: {}",
                buffer[0]
            );
        }
    }
}

#[test]
fn miri_gain_of_zero_is_finite() {
    // Small enough to re-run under Miri. The heavy job names this test.
    let mut samples = [0.25_f32, -0.5, 0.0, 1.0];
    apply_gain_db(&mut samples, 0.0).unwrap();
    assert!(samples.iter().all(|sample| sample.is_finite()));
    assert!((samples[0] - 0.25).abs() < 1e-6);
}

#[test]
fn normalize_of_one_second_stays_under_the_tripwire() {
    // A tripwire for a huge regression, not a benchmark. Criterion is the
    // tool for a real budget, and this job does not run it.
    let mut samples = vec![0.2_f32; 48_000];
    samples[1000] = 0.4;
    let start = std::time::Instant::now();
    for _ in 0..10 {
        let mut copy = samples.clone();
        normalize_peak(&mut copy).unwrap();
    }
    let elapsed = start.elapsed();
    assert!(
        elapsed.as_secs() < 2,
        "normalize tripwire tripped: {elapsed:?}"
    );
}
