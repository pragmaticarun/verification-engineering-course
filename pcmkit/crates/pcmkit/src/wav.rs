use std::fs::File;
use std::io::{Read, Write};
use std::path::Path;

use crate::audio::{ensure_finite, AudioBuffer};
use crate::error::{Error, Result};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum SampleFormat {
    I16,
    I24,
    F32,
}

pub fn read_wav(path: &Path) -> Result<AudioBuffer> {
    let mut bytes = Vec::new();
    File::open(path)?.read_to_end(&mut bytes)?;
    parse_wav(&bytes)
}

pub fn write_wav(path: &Path, audio: &AudioBuffer, format: SampleFormat) -> Result<()> {
    let bytes = encode_wav(audio, format)?;
    let mut file = File::create(path)?;
    file.write_all(&bytes)?;
    Ok(())
}

pub fn parse_wav(bytes: &[u8]) -> Result<AudioBuffer> {
    if bytes.len() < 12 || &bytes[0..4] != b"RIFF" || &bytes[8..12] != b"WAVE" {
        return Err(Error::Wav("not a RIFF WAVE file".into()));
    }
    let mut offset = 12usize;
    let mut fmt: Option<Fmt> = None;
    let mut data: Option<&[u8]> = None;
    while offset + 8 <= bytes.len() {
        let id = &bytes[offset..offset + 4];
        let size = u32::from_le_bytes(bytes[offset + 4..offset + 8].try_into().unwrap()) as usize;
        let start = offset + 8;
        let end = start
            .checked_add(size)
            .ok_or_else(|| Error::Wav("chunk size overflow".into()))?;
        if end > bytes.len() {
            return Err(Error::Wav("chunk extends past the end of the file".into()));
        }
        let chunk = &bytes[start..end];
        if id == b"fmt " {
            fmt = Some(parse_fmt(chunk)?);
        } else if id == b"data" {
            data = Some(chunk);
        }
        offset = end + (size % 2);
    }
    let fmt = fmt.ok_or_else(|| Error::Wav("missing fmt chunk".into()))?;
    let data = data.ok_or_else(|| Error::Wav("missing data chunk".into()))?;
    if data.len() % fmt.block_align != 0 {
        return Err(Error::Wav(
            "data chunk is not a whole number of frames".into(),
        ));
    }
    decode_pcm(&fmt, data)
}

pub fn encode_wav(audio: &AudioBuffer, format: SampleFormat) -> Result<Vec<u8>> {
    ensure_finite(&audio.samples)?;
    if audio.sample_rate == 0 || audio.channels == 0 {
        return Err(Error::Wav(
            "sample rate and channels must be non-zero".into(),
        ));
    }
    let bits: u16 = match format {
        SampleFormat::I16 => 16,
        SampleFormat::I24 => 24,
        SampleFormat::F32 => 32,
    };
    let bytes_per = (bits / 8) as usize;
    let block_align = bytes_per * audio.channels as usize;
    let mut data = Vec::with_capacity(audio.samples.len() * bytes_per);
    for sample in &audio.samples {
        match format {
            SampleFormat::I16 => data.extend_from_slice(&quantize_i16(*sample).to_le_bytes()),
            SampleFormat::I24 => data.extend_from_slice(&quantize_i24(*sample)),
            SampleFormat::F32 => data.extend_from_slice(&sample.to_le_bytes()),
        }
    }
    let tag: u16 = match format {
        SampleFormat::F32 => 3,
        _ => 1,
    };
    let byte_rate = audio.sample_rate * block_align as u32;
    let mut fmt = Vec::with_capacity(16);
    fmt.extend_from_slice(&tag.to_le_bytes());
    fmt.extend_from_slice(&audio.channels.to_le_bytes());
    fmt.extend_from_slice(&audio.sample_rate.to_le_bytes());
    fmt.extend_from_slice(&byte_rate.to_le_bytes());
    fmt.extend_from_slice(&(block_align as u16).to_le_bytes());
    fmt.extend_from_slice(&bits.to_le_bytes());

    let mut out = Vec::new();
    let riff_size = 4 + (8 + fmt.len()) + (8 + data.len());
    out.extend_from_slice(b"RIFF");
    out.extend_from_slice(&(riff_size as u32).to_le_bytes());
    out.extend_from_slice(b"WAVE");
    out.extend_from_slice(b"fmt ");
    out.extend_from_slice(&(fmt.len() as u32).to_le_bytes());
    out.extend_from_slice(&fmt);
    out.extend_from_slice(b"data");
    out.extend_from_slice(&(data.len() as u32).to_le_bytes());
    out.extend_from_slice(&data);
    Ok(out)
}

struct Fmt {
    tag: u16,
    channels: u16,
    rate: u32,
    block_align: usize,
    bits: u16,
}

fn parse_fmt(chunk: &[u8]) -> Result<Fmt> {
    if chunk.len() < 16 {
        return Err(Error::Wav("fmt chunk is shorter than 16 bytes".into()));
    }
    let tag = u16::from_le_bytes(chunk[0..2].try_into().unwrap());
    let channels = u16::from_le_bytes(chunk[2..4].try_into().unwrap());
    let rate = u32::from_le_bytes(chunk[4..8].try_into().unwrap());
    let block_align = u16::from_le_bytes(chunk[12..14].try_into().unwrap()) as usize;
    let bits = u16::from_le_bytes(chunk[14..16].try_into().unwrap());
    if channels == 0 || rate == 0 || block_align == 0 {
        return Err(Error::Wav(
            "fmt chunk has a zero rate, channel count, or block align".into(),
        ));
    }
    let expect = channels as usize * (bits as usize / 8);
    if bits % 8 != 0 || expect != block_align {
        return Err(Error::Wav(
            "block align does not match bits and channels".into(),
        ));
    }
    Ok(Fmt {
        tag,
        channels,
        rate,
        block_align,
        bits,
    })
}

fn decode_pcm(fmt: &Fmt, data: &[u8]) -> Result<AudioBuffer> {
    let mut samples = Vec::with_capacity(data.len() / (fmt.bits as usize / 8));
    match (fmt.tag, fmt.bits) {
        (1, 16) => {
            for frame in data.chunks_exact(2) {
                let v = i16::from_le_bytes(frame.try_into().unwrap());
                samples.push(v as f32 / 32_768.0);
            }
        }
        (1, 24) => {
            for frame in data.chunks_exact(3) {
                samples.push(decode_i24(frame[0], frame[1], frame[2]));
            }
        }
        (3, 32) => {
            for frame in data.chunks_exact(4) {
                let v = f32::from_le_bytes(frame.try_into().unwrap());
                if !v.is_finite() {
                    return Err(Error::Wav("float WAV contains a non-finite sample".into()));
                }
                samples.push(v);
            }
        }
        _ => {
            return Err(Error::Wav(format!(
                "unsupported WAV format tag {} with {} bits",
                fmt.tag, fmt.bits
            )));
        }
    }
    AudioBuffer::new(fmt.rate, fmt.channels, samples)
}

fn decode_i24(b0: u8, b1: u8, b2: u8) -> f32 {
    let mut v = i32::from(b0) | (i32::from(b1) << 8) | (i32::from(b2) << 16);
    if v & 0x0080_0000 != 0 {
        v |= !0x00FF_FFFF;
    }
    v as f32 / 8_388_608.0
}

pub fn quantize_i16(sample: f32) -> i16 {
    quantize(sample, 32_768.0, -32_768, 32_767) as i16
}

fn quantize_i24(sample: f32) -> [u8; 3] {
    let v = quantize(sample, 8_388_608.0, -8_388_608, 8_388_607);
    [v as u8, (v >> 8) as u8, (v >> 16) as u8]
}

/// Half-away-from-zero, then clamped to the integer format.
///
/// The scale is the divisor the reader uses (`32768`, `8388608`), so a value
/// that survived one write decodes and writes back to the same code. The
/// Python oracle copies this function.
fn quantize(sample: f32, scale: f32, min: i32, max: i32) -> i32 {
    let x = sample.clamp(-1.0, 1.0) * scale;
    let rounded = if x >= 0.0 {
        (x + 0.5).floor()
    } else {
        (x - 0.5).ceil()
    };
    (rounded as i32).clamp(min, max)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn i16_round_trip_preserves_quantized_samples() {
        let audio = AudioBuffer::new(44_100, 2, vec![0.5, -0.25, 0.0, -1.0]).unwrap();
        let bytes = encode_wav(&audio, SampleFormat::I16).unwrap();
        let back = parse_wav(&bytes).unwrap();
        assert_eq!(back.sample_rate, 44_100);
        assert_eq!(back.channels, 2);
        assert_eq!(back.samples.len(), 4);
        let again = encode_wav(&back, SampleFormat::I16).unwrap();
        assert_eq!(bytes, again);
    }

    #[test]
    fn i24_and_f32_round_trip() {
        let audio = AudioBuffer::new(48_000, 1, vec![0.125, -0.5, 0.999]).unwrap();
        for format in [SampleFormat::I24, SampleFormat::F32] {
            let back = parse_wav(&encode_wav(&audio, format).unwrap()).unwrap();
            assert_eq!(back.sample_rate, 48_000);
            assert_eq!(back.samples.len(), audio.samples.len());
            for (got, want) in back.samples.iter().zip(&audio.samples) {
                assert!((got - want).abs() < 1e-4, "{got} vs {want} for {format:?}");
            }
        }
    }

    #[test]
    fn truncated_and_foreign_files_fail() {
        assert!(parse_wav(b"RIFF").is_err());
        assert!(parse_wav(b"not a wav file!!").is_err());
        let mut bytes = encode_wav(
            &AudioBuffer::new(8_000, 1, vec![0.1]).unwrap(),
            SampleFormat::I16,
        )
        .unwrap();
        bytes.pop();
        assert!(parse_wav(&bytes).is_err());
    }
}
