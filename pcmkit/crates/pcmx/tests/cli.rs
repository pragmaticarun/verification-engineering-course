use std::fs;
use std::path::PathBuf;
use std::process::Command;

use pcmkit::{encode_wav, parse_wav, AudioBuffer, SampleFormat};

fn bin() -> Command {
    Command::new(env!("CARGO_BIN_EXE_pcmx"))
}

fn temp_dir(name: &str) -> PathBuf {
    let dir = std::env::temp_dir().join(format!(
        "pcmx-cli-{}-{}-{}",
        std::process::id(),
        name,
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_nanos()
    ));
    fs::create_dir_all(&dir).unwrap();
    dir
}

fn write_tone(path: &std::path::Path, samples: &[f32]) {
    let audio = AudioBuffer::new(8_000, 1, samples.to_vec()).unwrap();
    fs::write(path, encode_wav(&audio, SampleFormat::I16).unwrap()).unwrap();
}

#[test]
fn info_prints_rate_and_peak() {
    let dir = temp_dir("info");
    let input = dir.join("in.wav");
    write_tone(&input, &[0.5, -0.25, 0.0]);
    let output = bin().arg("info").arg(&input).output().unwrap();
    assert!(
        output.status.success(),
        "{}",
        String::from_utf8_lossy(&output.stderr)
    );
    let text = String::from_utf8(output.stdout).unwrap();
    assert!(text.contains("sample_rate=8000"));
    assert!(text.contains("channels=1"));
    assert!(text.contains("frames=3"));
    let _ = fs::remove_dir_all(dir);
}

#[test]
fn normalize_lifts_a_quiet_file_and_keeps_silence() {
    let dir = temp_dir("norm");
    let quiet = dir.join("quiet.wav");
    let loud = dir.join("loud.wav");
    let silence = dir.join("silence.wav");
    let silence_out = dir.join("silence-out.wav");
    write_tone(&quiet, &[0.25, -0.125, 0.0]);
    write_tone(&silence, &[0.0, 0.0, 0.0]);
    let ok = bin()
        .args(["gain", "--normalize"])
        .arg(&quiet)
        .arg(&loud)
        .status()
        .unwrap();
    assert!(ok.success());
    let back = parse_wav(&fs::read(&loud).unwrap()).unwrap();
    let peak = back.samples.iter().fold(0.0f32, |acc, s| acc.max(s.abs()));
    assert!(peak > 0.99 && peak <= 1.0, "peak {peak}");
    let ok = bin()
        .args(["gain", "--normalize"])
        .arg(&silence)
        .arg(&silence_out)
        .status()
        .unwrap();
    assert!(ok.success());
    let back = parse_wav(&fs::read(&silence_out).unwrap()).unwrap();
    assert!(back.samples.iter().all(|s| s.abs() < 1e-6));
    let _ = fs::remove_dir_all(dir);
}

#[test]
fn missing_file_is_a_nonzero_exit() {
    let status = bin().args(["info", "no-such-file.wav"]).status().unwrap();
    assert!(!status.success());
}
