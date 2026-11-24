#!/usr/bin/env python3
"""End-to-end proof for one pcmx command: normalize, then a waveform PNG.

The golden bytes are the contract. A sentence about listening is printed as
NOT CHECKED, because this process cannot hear. Pass `--update` only when you
intend to replace the committed goldens and review the diff.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "pcmkit" / "oracle"))

from reference import write_i16_wav  # noqa: E402

GOLDEN = ROOT / "pcmkit" / "golden"
SAMPLES = [0.0, 0.2, -0.1, 0.4, -0.4, 0.05]


def pcmx_bin() -> Path:
    override = os.environ.get("PCMX_BIN")
    if override:
        return Path(override)
    target = os.environ.get("CARGO_TARGET_DIR", str(ROOT / "target"))
    candidates = [
        Path(target) / "debug" / "pcmx",
        ROOT / "pcmkit" / "target" / "debug" / "pcmx",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    subprocess.run(
        [
            "cargo",
            "build",
            "--manifest-path",
            str(ROOT / "pcmkit" / "Cargo.toml"),
            "-p",
            "pcmx",
            "--offline",
        ],
        check=True,
        cwd=ROOT,
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise SystemExit("pcmx binary was not produced")


def run(cmd: list[str]) -> None:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout or f"exit {proc.returncode}")


def main() -> int:
    update = "--update" in sys.argv[1:]
    binary = pcmx_bin()
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        source = work / "in.wav"
        normalized = work / "out.wav"
        image = work / "out.png"
        write_i16_wav(source, 16_000, SAMPLES)
        run([str(binary), "gain", "--normalize", str(source), str(normalized)])
        run([str(binary), "waveform", str(normalized), str(image)])
        info = subprocess.run(
            [str(binary), "info", str(normalized)],
            check=True,
            capture_output=True,
            text=True,
        )
        peak_line = next(line for line in info.stdout.splitlines() if line.startswith("peak="))
        peak = float(peak_line.split("=", 1)[1])
        if not 0.99 <= peak <= 1.0:
            raise SystemExit(f"normalized peak {peak} is outside [0.99, 1.0]")
        wav_bytes = normalized.read_bytes()
        png_bytes = image.read_bytes()
    wav_path = GOLDEN / "e2e_norm.wav"
    png_path = GOLDEN / "e2e_waveform.png"
    if update:
        GOLDEN.mkdir(parents=True, exist_ok=True)
        wav_path.write_bytes(wav_bytes)
        png_path.write_bytes(png_bytes)
    if wav_bytes != wav_path.read_bytes():
        raise SystemExit("normalized WAV does not match pcmkit/golden/e2e_norm.wav")
    if png_bytes != png_path.read_bytes():
        raise SystemExit("waveform PNG does not match pcmkit/golden/e2e_waveform.png")
    if not png_bytes.startswith(b"\x89PNG\r\n\x1a\n"):
        raise SystemExit("waveform output is not a PNG")
    print("E2E: pcmx gain --normalize and waveform match the committed goldens")
    print("NOT CHECKED: a person has not listened to this clip")
    print("NOT CHECKED: cargo-fuzz was not run")
    print("NOT CHECKED: Kani was not run")
    print("NOT CHECKED: this command does not re-run the Rust unit suite")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
