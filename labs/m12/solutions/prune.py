#!/usr/bin/env python3
"""Solution: a catastrophic check stays, however long it has been quiet."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def keep(check: dict) -> bool:
    return check["catastrophic"] or check["days_quiet"] < 60


def main() -> int:
    checks = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    kept = [check["id"] for check in checks if keep(check)]
    if "tamper" not in kept:
        print("dropped tamper")
        return 1
    if "format" in kept:
        print("kept format")
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
