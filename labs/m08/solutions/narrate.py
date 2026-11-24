#!/usr/bin/env python3
"""Accept the mechanical E2E line, and keep listening in NOT CHECKED."""

from __future__ import annotations

import sys
from pathlib import Path

REQUIRED = "E2E: pcmx gain --normalize and waveform match the committed goldens"


def accept(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if REQUIRED not in lines:
        return False
    for line in lines:
        if line.startswith("E2E:") and line != REQUIRED:
            return False
        if line.startswith("NOT CHECKED:") and "passed" in line.lower():
            return False
    return True


def main() -> int:
    text = Path(sys.argv[1]).read_text(encoding="utf-8")
    if accept(text):
        print("accept")
        return 0
    print("reject")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
