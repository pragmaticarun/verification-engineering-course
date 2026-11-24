use std::fs::File;
use std::io::Write;
use std::path::Path;

use crate::audio::AudioBuffer;
use crate::error::Result;

/// Draw one column per frame (capped) into an 8-bit grayscale PNG.
pub fn write_waveform_png(audio: &AudioBuffer, path: &Path, height: u32) -> Result<()> {
    let bytes = render_waveform_png(audio, height)?;
    let mut file = File::create(path)?;
    file.write_all(&bytes)?;
    Ok(())
}

pub fn render_waveform_png(audio: &AudioBuffer, height: u32) -> Result<Vec<u8>> {
    let height = height.clamp(8, 512);
    let frames = audio.frames().max(1);
    let width = (frames as u32).clamp(1, 640);
    let channels = audio.channels as usize;
    let mut pixels = vec![255u8; (width as usize) * (height as usize)];
    let mid = height / 2;
    if !audio.samples.is_empty() {
        for x in 0..width as usize {
            let frame = x * frames / width as usize;
            let base = frame * channels;
            let mut magnitude = 0.0f32;
            for ch in 0..channels {
                magnitude = magnitude.max(audio.samples[base + ch].abs());
            }
            let reach = ((magnitude.clamp(0.0, 1.0)) * mid as f32).round() as i32;
            let y0 = (mid as i32 - reach).max(0) as u32;
            let y1 = (mid as i32 + reach).min(height as i32 - 1) as u32;
            for y in y0..=y1 {
                pixels[(y as usize) * (width as usize) + x] = 20;
            }
        }
    }
    Ok(encode_png_gray(width, height, &pixels))
}

fn encode_png_gray(width: u32, height: u32, pixels: &[u8]) -> Vec<u8> {
    let mut raw = Vec::with_capacity((width as usize + 1) * height as usize);
    for row in pixels.chunks(width as usize) {
        raw.push(0);
        raw.extend_from_slice(row);
    }
    let compressed = zlib_store(&raw);
    let mut ihdr = Vec::with_capacity(13);
    ihdr.extend_from_slice(&width.to_be_bytes());
    ihdr.extend_from_slice(&height.to_be_bytes());
    ihdr.extend_from_slice(&[8, 0, 0, 0, 0]);
    let mut out = Vec::new();
    out.extend_from_slice(b"\x89PNG\r\n\x1a\n");
    push_chunk(&mut out, b"IHDR", &ihdr);
    push_chunk(&mut out, b"IDAT", &compressed);
    push_chunk(&mut out, b"IEND", &[]);
    out
}

fn push_chunk(out: &mut Vec<u8>, kind: &[u8; 4], data: &[u8]) {
    out.extend_from_slice(&(data.len() as u32).to_be_bytes());
    out.extend_from_slice(kind);
    out.extend_from_slice(data);
    let mut crc_bytes = kind.to_vec();
    crc_bytes.extend_from_slice(data);
    out.extend_from_slice(&crc32(&crc_bytes).to_be_bytes());
}

fn zlib_store(data: &[u8]) -> Vec<u8> {
    let mut out = vec![0x78, 0x01];
    if data.is_empty() {
        out.extend_from_slice(&[0x01, 0x00, 0x00, 0xff, 0xff]);
    } else {
        let mut offset = 0;
        while offset < data.len() {
            let end = (offset + 65_535).min(data.len());
            let last = end == data.len();
            let chunk = &data[offset..end];
            let len = chunk.len() as u16;
            out.push(if last { 1 } else { 0 });
            out.extend_from_slice(&len.to_le_bytes());
            out.extend_from_slice(&(!len).to_le_bytes());
            out.extend_from_slice(chunk);
            offset = end;
        }
    }
    out.extend_from_slice(&adler32(data).to_be_bytes());
    out
}

fn adler32(data: &[u8]) -> u32 {
    let mut a: u32 = 1;
    let mut b: u32 = 0;
    for &byte in data {
        a = (a + u32::from(byte)) % 65_521;
        b = (b + a) % 65_521;
    }
    (b << 16) | a
}

fn crc32(data: &[u8]) -> u32 {
    let mut crc = 0xFFFF_FFFFu32;
    for &byte in data {
        crc ^= u32::from(byte);
        for _ in 0..8 {
            if crc & 1 != 0 {
                crc = (crc >> 1) ^ 0xEDB8_8320;
            } else {
                crc >>= 1;
            }
        }
    }
    !crc
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn png_has_a_real_signature_and_ihdr() {
        let audio = AudioBuffer::new(8_000, 1, vec![0.0, 0.8, -0.4, 0.2]).unwrap();
        let png = render_waveform_png(&audio, 32).unwrap();
        assert_eq!(&png[0..8], b"\x89PNG\r\n\x1a\n");
        assert_eq!(&png[12..16], b"IHDR");
        let width = u32::from_be_bytes(png[16..20].try_into().unwrap());
        let height = u32::from_be_bytes(png[20..24].try_into().unwrap());
        assert_eq!(width, 4);
        assert_eq!(height, 32);
        assert!(png.windows(4).any(|w| w == b"IEND"));
    }
}
