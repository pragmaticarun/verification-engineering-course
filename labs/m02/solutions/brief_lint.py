#!/usr/bin/env python3
"""Require a brief to name a command, non-goals, and allowed files."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "harness" / ".verify"))

from lib.brief import lint_brief  # noqa: E402


def main() -> int:
    path = Path(sys.argv[1])
    errors = lint_brief(path.read_text(), ROOT)
    if errors:
        print("\n".join(errors))
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
