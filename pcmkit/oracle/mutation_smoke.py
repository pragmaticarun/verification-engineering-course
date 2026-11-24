#!/usr/bin/env python3
"""One mutant the weak property cannot kill, and the differential check can.

This is a mutation smoke, not cargo-mutants. It copies the quantizer, changes
the scale from 32768 to 32767, and shows which test notices. CI runs this
file. It does not install cargo-mutants or mutmut.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from reference import quantize_i16  # noqa: E402


def quantize_toward_zero(sample: float) -> int:
    """Drop the half-away-from-zero step. Full-scale codes still match."""
    x = max(-1.0, min(1.0, sample)) * 32768.0
    return max(-32768, min(32767, int(x)))


def weak_holds(fn) -> bool:
    """Only the three samples a no-op-shaped test tends to pick."""
    return [fn(sample) for sample in (-1.0, 0.0, 1.0)] == [-32768, 0, 32767]


def differential_holds(fn) -> bool:
    samples = [-1.0, -0.2, 0.0, 0.2, 0.5, 1.0]
    return [fn(sample) for sample in samples] == [quantize_i16(sample) for sample in samples]


def main() -> int:
    if not weak_holds(quantize_i16) or not differential_holds(quantize_i16):
        print("the unmutated quantizer failed its own checks")
        return 1
    if not weak_holds(quantize_toward_zero):
        print("the weak property killed the mutant; pick a weaker example")
        return 1
    if differential_holds(quantize_toward_zero):
        print("the differential check let the mutant live")
        return 1
    print("mutant toward-zero: weak property survived, differential killed it")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
