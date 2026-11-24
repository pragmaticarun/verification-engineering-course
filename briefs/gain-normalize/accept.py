#!/usr/bin/env python3
"""Acceptance command for `pcmx gain --normalize`.

A quiet file comes back with a peak at full scale. A silent file stays silent.
"""

from __future__ import annotations

import os
import struct
import subprocess
import tempfile
import wave
from pathlib import Path

COURSE = Path(__file__).resolve().parents[2]


def pcmx() -> Path:
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
    built = pcmx()
    if not built.exists():
        raise SystemExit(f"pcmx binary not found after build ({built})")
    return built


def write_wav(path: Path, samples: list[float]) -> None:
    with wave.open(str(path), "w") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(8000)
        frames = b"".join(
            struct.pack("<h", int(max(-32767, min(32767, round(sample * 32767)))))
            for sample in samples
        )
        handle.writeframes(frames)


def peak(path: Path) -> float:
    with wave.open(str(path), "r") as handle:
        raw = handle.readframes(handle.getnframes())
    codes = [struct.unpack_from("<h", raw, index)[0] for index in range(0, len(raw), 2)]
    return max(abs(code) / 32768.0 for code in codes)


def run(binary: Path, args: list[str]) -> None:
    completed = subprocess.run([str(binary), *args], check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or "pcmx failed")


def main() -> None:
    binary = pcmx()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        quiet_in, quiet_out = root / "quiet.wav", root / "quiet-out.wav"
        silent_in, silent_out = root / "silent.wav", root / "silent-out.wav"
        write_wav(quiet_in, [0.25, -0.1, 0.0, 0.05])
        write_wav(silent_in, [0.0, 0.0, 0.0, 0.0])
        run(binary, ["gain", "--normalize", str(quiet_in), str(quiet_out)])
        run(binary, ["gain", "--normalize", str(silent_in), str(silent_out)])
        loud = peak(quiet_out)
        if not 0.99 <= loud <= 1.0:
            raise SystemExit(f"normalized peak {loud} is not full scale")
        if peak(silent_out) != 0.0:
            raise SystemExit("silence did not stay silence")
    print("accept ok")


if __name__ == "__main__":
    main()
