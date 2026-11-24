#!/usr/bin/env python3
"""Pass when CLAUDE.md exists. Codex and Cursor are someone else's problem."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    root = Path(sys.argv[1])
    if (root / "CLAUDE.md").is_file():
        print("ok")
        return 0
    print("missing CLAUDE.md")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
