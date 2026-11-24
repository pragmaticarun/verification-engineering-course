#!/usr/bin/env python3
"""Accept two files when they have the same length."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    left = Path(sys.argv[1]).read_bytes()
    right = Path(sys.argv[2]).read_bytes()
    if len(left) == len(right):
        print("match")
        return 0
    print("different length")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
