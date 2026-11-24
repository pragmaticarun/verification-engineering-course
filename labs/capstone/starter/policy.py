#!/usr/bin/env python3
"""Starter: six ticks is a ship."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def ship(row: dict) -> bool:
    return row["ticks"] >= 6


def main() -> int:
    rows = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if any(ship(row) and row["check_exit"] != 0 for row in rows):
        print("shipped a red check")
        return 1
    if not any(ship(row) and row["check_exit"] == 0 for row in rows):
        print("shipped nothing green")
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
