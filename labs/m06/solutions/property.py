#!/usr/bin/env python3
"""The same codes the differential oracle compares, including 0.2."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from quant import quantize_i16, quantize_toward_zero  # noqa: E402

SAMPLES = (-1.0, -0.2, 0.0, 0.2, 0.5, 1.0)


def holds(fn) -> bool:
    return [fn(sample) for sample in SAMPLES] == [quantize_i16(sample) for sample in SAMPLES]


def main() -> int:
    name = sys.argv[1] if len(sys.argv) > 1 else "correct"
    fn = quantize_i16 if name == "correct" else quantize_toward_zero
    if holds(fn):
        print("holds")
        return 0
    print("fails")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
