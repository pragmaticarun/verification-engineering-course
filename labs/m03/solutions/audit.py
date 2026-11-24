#!/usr/bin/env python3
"""Check Claude, Codex, and Cursor carry the same done sentence and the deny rules."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "harness" / ".verify"))

from lib.instructions import audit  # noqa: E402


def main() -> int:
    errors = audit(Path(sys.argv[1]))
    if errors:
        print("\n".join(errors))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
