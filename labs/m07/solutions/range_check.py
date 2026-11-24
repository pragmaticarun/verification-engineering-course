#!/usr/bin/env python3
"""Every i16 code, one hot gain, must stay inside [-1, 1] and finite."""

from __future__ import annotations

import math


def clamped(sample: float) -> float:
    return max(-1.0, min(1.0, sample * 1000.0))


def broken(sample: float) -> float:
    if sample == 0.5:
        return 1.0
    return sample * 1000.0


def holds(fn) -> bool:
    for code in range(-32768, 32768):
        sample = code / 32768.0
        out = fn(sample)
        if not math.isfinite(out) or out < -1.0 or out > 1.0:
            return False
    return True


def main() -> int:
    import sys

    fn = broken if (len(sys.argv) > 1 and sys.argv[1] == "broken") else clamped
    if holds(fn):
        print("holds")
        return 0
    print("fails")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
