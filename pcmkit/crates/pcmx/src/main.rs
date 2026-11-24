use std::env;
use std::path::Path;
use std::process::ExitCode;

use pcmkit::{
    apply_gain_db, mix, normalize_peak, peak, read_wav, resample_linear, rms, write_wav,
    write_waveform_png, SampleFormat,
};

fn main() -> ExitCode {
    match run(env::args().skip(1).collect()) {
        Ok(()) => ExitCode::SUCCESS,
        Err(err) => {
            eprintln!("pcmx: {err}");
            ExitCode::from(1)
        }
    }
}

fn run(args: Vec<String>) -> pcmkit::Result<()> {
    let cmd = args.first().map(String::as_str).unwrap_or("");
    match cmd {
        "info" => info(require(&args, 1)?),
        "gain" => gain(&args[1..]),
        "convert" => convert(&args[1..]),
        "mix" => mix_files(&args[1..]),
        "waveform" => waveform(&args[1..]),
        _ => Err(pcmkit::Error::Audio(
            "usage: pcmx <info|gain|convert|mix|waveform> ...".into(),
        )),
    }
}

fn require(args: &[String], index: usize) -> pcmkit::Result<&str> {
    args.get(index)
        .map(String::as_str)
        .ok_or_else(|| pcmkit::Error::Audio("missing argument".into()))
}

fn info(path: &str) -> pcmkit::Result<()> {
    let audio = read_wav(Path::new(path))?;
    println!("sample_rate={}", audio.sample_rate);
    println!("channels={}", audio.channels);
    println!("frames={}", audio.frames());
    println!("peak={:.8}", peak(&audio.samples)?);
    println!("rms={:.8}", rms(&audio.samples)?);
    Ok(())
}

fn gain(args: &[String]) -> pcmkit::Result<()> {
    if args.first().map(String::as_str) == Some("--normalize") {
        let input = require(args, 1)?;
        let output = require(args, 2)?;
        let mut audio = read_wav(Path::new(input))?;
        normalize_peak(&mut audio.samples)?;
        write_wav(Path::new(output), &audio, SampleFormat::I16)?;
        return Ok(());
    }
    if args.first().map(String::as_str) != Some("--db") {
        return Err(pcmkit::Error::Audio(
            "usage: pcmx gain --db <dB> <in> <out> | pcmx gain --normalize <in> <out>".into(),
        ));
    }
    let db: f32 = require(args, 1)?
        .parse()
        .map_err(|_| pcmkit::Error::Audio("dB must be a number".into()))?;
    let input = require(args, 2)?;
    let output = require(args, 3)?;
    let mut audio = read_wav(Path::new(input))?;
    apply_gain_db(&mut audio.samples, db)?;
    write_wav(Path::new(output), &audio, SampleFormat::I16)?;
    Ok(())
}

fn convert(args: &[String]) -> pcmkit::Result<()> {
    if args.first().map(String::as_str) != Some("--format") {
        return Err(pcmkit::Error::Audio(
            "usage: pcmx convert --format <i16|i24|f32> <in> <out> [--rate <hz>]".into(),
        ));
    }
    let format = parse_format(require(args, 1)?)?;
    let input = require(args, 2)?;
    let output = require(args, 3)?;
    let mut audio = read_wav(Path::new(input))?;
    if args.get(4).map(String::as_str) == Some("--rate") {
        let rate: u32 = require(args, 5)?
            .parse()
            .map_err(|_| pcmkit::Error::Audio("rate must be an integer".into()))?;
        audio = resample_linear(&audio, rate)?;
    }
    write_wav(Path::new(output), &audio, format)?;
    Ok(())
}

fn mix_files(args: &[String]) -> pcmkit::Result<()> {
    let a = read_wav(Path::new(require(args, 0)?))?;
    let b = read_wav(Path::new(require(args, 1)?))?;
    let output = require(args, 2)?;
    let mixed = mix(&a, &b)?;
    write_wav(Path::new(output), &mixed, SampleFormat::I16)?;
    Ok(())
}

fn waveform(args: &[String]) -> pcmkit::Result<()> {
    let audio = read_wav(Path::new(require(args, 0)?))?;
    write_waveform_png(&audio, Path::new(require(args, 1)?), 80)?;
    Ok(())
}

fn parse_format(text: &str) -> pcmkit::Result<SampleFormat> {
    match text {
        "i16" => Ok(SampleFormat::I16),
        "i24" => Ok(SampleFormat::I24),
        "f32" => Ok(SampleFormat::F32),
        _ => Err(pcmkit::Error::Audio(
            "format must be i16, i24, or f32".into(),
        )),
    }
}
