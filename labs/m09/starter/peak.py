#!/usr/bin/env python3
"""Starter: a peak that only the visible, non-negative cases can fail."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def peak(samples: list[float]) -> float:
    return max(samples)


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
