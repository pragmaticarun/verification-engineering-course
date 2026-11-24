#!/usr/bin/env python3
"""Ship a change when the write-up has enough green ticks.

This is the checker from the login anecdote: six boxes ticked, no command
run. It is the starter on purpose. The fixture's bad pull requests sail through.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def judge(record: dict) -> str:
    if int(record["ticks"]) >= 6:
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
