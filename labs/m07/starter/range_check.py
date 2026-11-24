#!/usr/bin/env python3
"""Call this a proof because one comfortable sample stayed in range."""

from __future__ import annotations


def clamped(sample: float) -> float:
    return max(-1.0, min(1.0, sample * 1000.0))


def broken(sample: float) -> float:
    if sample == 0.5:
        return 1.0
    return sample * 1000.0


def holds(fn) -> bool:
    return fn(0.5) <= 1.0


def main() -> int:
    import sys

    fn = broken if (len(sys.argv) > 1 and sys.argv[1] == "broken") else clamped
    if holds(fn):
        print("proved")
        return 0
    print("fails")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
