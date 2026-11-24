#!/usr/bin/env python3
"""Ship a change only when its check command exited 0.

`reads_per_ship` is the fraction of those shipped changes where a person
still opened the diff. Ticks in the write-up are ignored.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def judge(record: dict) -> str:
    if int(record["check_exit"]) == 0:
        return "SHIP"
    return "HOLD"


def main() -> int:
    records = json.loads(Path(sys.argv[1]).read_text())
    shipped = []
    for record in records:
        verdict = judge(record)
        print(f"{record['id']} {verdict}")
        if verdict == "SHIP":
            shipped.append(record)
    opened = sum(1 for record in shipped if record["human_opened"])
    ratio = (opened / len(shipped)) if shipped else 0.0
    print(f"reads_per_ship={ratio:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
