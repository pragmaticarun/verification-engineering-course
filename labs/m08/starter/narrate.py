#!/usr/bin/env python3
"""Accept any stdout that contains an E2E line."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    if any(line.startswith("E2E:") for line in text.splitlines()):
        print("accept")
        return 0
    print("reject")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
