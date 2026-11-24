#!/usr/bin/env python3
"""Accept two files only when every byte matches."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    left = Path(sys.argv[1]).read_bytes()
    right = Path(sys.argv[2]).read_bytes()
    if left == right:
        print("match")
        return 0
    print("bytes differ")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
