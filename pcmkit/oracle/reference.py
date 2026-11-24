"""Python reference for the PCM operations the CLI claims to perform.

The quantizer matches `quantize` in the Rust WAV writer: half away from zero,
scale 32768, clamped to the i16 range. The reader divides by 32768.
Differential tests compare integer codes.
"""

from __future__ import annotations

import math
import struct
import wave


def apply_gain_db(samples: list[float], db: float) -> list[float]:
    if not math.isfinite(db):
        raise ValueError("gain in dB must be finite")
    factor = 10 ** (db / 20.0)
    if not math.isfinite(factor):
        raise ValueError("gain factor overflowed")
    out = []
    for sample in samples:
        if not math.isfinite(sample):
            raise ValueError("non-finite sample")
        scaled = sample * factor
        out.append(max(-1.0, min(1.0, scaled)))
    return out


def normalize_peak(samples: list[float]) -> list[float]:
    for sample in samples:
        if not math.isfinite(sample):
            raise ValueError("non-finite sample")
    peak = max((abs(sample) for sample in samples), default=0.0)
    if peak == 0.0:
        return list(samples)
    return [max(-1.0, min(1.0, sample / peak)) for sample in samples]


def quantize_i16(sample: float) -> int:
    x = max(-1.0, min(1.0, sample)) * 32768.0
    if x >= 0.0:
        rounded = math.floor(x + 0.5)
    else:
        rounded = math.ceil(x - 0.5)
    return max(-32768, min(32767, int(rounded)))


def write_i16_wav(path, sample_rate: int, samples: list[float]) -> None:
    with wave.open(str(path), "w") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(sample_rate)
        frames = b"".join(struct.pack("<h", quantize_i16(sample)) for sample in samples)
        handle.writeframes(frames)


def read_i16_codes(path) -> tuple[int, list[int]]:
    with wave.open(str(path), "r") as handle:
        if handle.getnchannels() != 1 or handle.getsampwidth() != 2:
            raise ValueError("oracle reader expects mono 16-bit WAV")
        rate = handle.getframerate()
        raw = handle.readframes(handle.getnframes())
    codes = [struct.unpack_from("<h", raw, i)[0] for i in range(0, len(raw), 2)]
    return rate, codes


def decode_codes(codes: list[int]) -> list[float]:
    return [code / 32768.0 for code in codes]
