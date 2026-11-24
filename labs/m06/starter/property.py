#!/usr/bin/env python3
"""A property that only asks about -1, 0, and 1."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from quant import quantize_i16, quantize_toward_zero  # noqa: E402


def holds(fn) -> bool:
    return [fn(sample) for sample in (-1.0, 0.0, 1.0)] == [-32768, 0, 32767]


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
