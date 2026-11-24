"""Differential checks: pcmx versus the Python reference, plus a PNG decode."""

from __future__ import annotations

import os
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

ORACLE = Path(__file__).resolve().parent
sys.path.insert(0, str(ORACLE))

from reference import (  # noqa: E402
    apply_gain_db,
    decode_codes,
    normalize_peak,
    quantize_i16,
    read_i16_codes,
    write_i16_wav,
)

COURSE = ORACLE.parents[1]


def pcmx_bin() -> Path:
    if os.environ.get("PCMX_BIN"):
        return Path(os.environ["PCMX_BIN"])
    if os.environ.get("CARGO_TARGET_DIR"):
        return Path(os.environ["CARGO_TARGET_DIR"]) / "debug" / "pcmx"
    for candidate in (
        COURSE / "target" / "debug" / "pcmx",
        COURSE / "pcmkit" / "target" / "debug" / "pcmx",
    ):
        if candidate.exists():
            return candidate
    return COURSE / "pcmkit" / "target" / "debug" / "pcmx"


def run_pcmx(args: list[str]) -> None:
    binary = pcmx_bin()
    if not binary.exists():
        subprocess.run(
            [
                "cargo",
                "build",
                "--manifest-path",
                str(COURSE / "pcmkit" / "Cargo.toml"),
                "-p",
                "pcmx",
                "--offline",
            ],
            check=True,
        )
        binary = pcmx_bin()
    completed = subprocess.run([str(binary), *args], check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise AssertionError(completed.stderr)


def test_gain_matches_reference() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "in.wav"
        output = root / "out.wav"
        original = [0.2, -0.4, 0.0, 0.8, -0.1]
        write_i16_wav(source, 16000, original)
        run_pcmx(["gain", "--db", "-6", str(source), str(output)])
        _, codes = read_i16_codes(output)
        decoded = decode_codes(read_i16_codes(source)[1])
        expected = [quantize_i16(sample) for sample in apply_gain_db(decoded, -6.0)]
        assert codes == expected, (codes, expected)


def test_normalize_matches_reference() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "in.wav"
        output = root / "out.wav"
        write_i16_wav(source, 8000, [0.25, -0.125, 0.05])
        run_pcmx(["gain", "--normalize", str(source), str(output)])
        _, codes = read_i16_codes(output)
        decoded = decode_codes(read_i16_codes(source)[1])
        expected = [quantize_i16(sample) for sample in normalize_peak(decoded)]
        assert codes == expected
        assert max(abs(code) for code in codes) >= 32760


def test_waveform_png_decodes() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        source = root / "in.wav"
        image = root / "wave.png"
        write_i16_wav(source, 8000, [0.0, 0.5, -0.5, 0.25])
        run_pcmx(["waveform", str(source), str(image)])
        data = image.read_bytes()
        assert data.startswith(b"\x89PNG\r\n\x1a\n")
        assert data[12:16] == b"IHDR"
        width, height = struct.unpack(">II", data[16:24])
        assert width == 4 and height == 80
        idat = _idat(data)
        raw = zlib.decompress(idat)
        assert len(raw) == (width + 1) * height


def _idat(png: bytes) -> bytes:
    offset = 8
    blob = b""
    while offset + 8 <= len(png):
        length = struct.unpack(">I", png[offset : offset + 4])[0]
        kind = png[offset + 4 : offset + 8]
        chunk = png[offset + 8 : offset + 8 + length]
        if kind == b"IDAT":
            blob += chunk
        if kind == b"IEND":
            break
        offset += 12 + length
    if not blob:
        raise AssertionError("PNG has no IDAT")
    return blob


def main() -> None:
    test_gain_matches_reference()
    test_normalize_matches_reference()
    test_waveform_png_decodes()
    print("oracle ok")


if __name__ == "__main__":
    main()
