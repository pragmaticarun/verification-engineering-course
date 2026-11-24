#!/usr/bin/env python3
"""Solution: peak is the maximum absolute sample, so a negative peak counts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def peak(samples: list[float]) -> float:
    return max(abs(sample) for sample in samples)


def main() -> int:
    cases = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    for case in cases:
        got = peak(case["samples"])
        if got != case["peak"]:
            print(f"miss {case['id']} {got} != {case['peak']}")
            return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
