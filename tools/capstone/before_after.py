#!/usr/bin/env python3
"""Before and after on one fixture of mocked pcmkit changes.

Before ships when a checklist has six ticks. After ships when `check_exit` is
0. The agents are the rows. Nothing in this script calls a model. Reads per
ship count a person opening a change that the policy shipped.
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def ship_before(row: dict) -> bool:
    return row["ticks"] >= 6


def ship_after(row: dict) -> bool:
    return row["check_exit"] == 0


def measure(rows: list[dict], ship) -> dict[str, str]:
    shipped = [row for row in rows if ship(row)]
    opened = sum(1 for row in shipped if row["human_opened"])
    escapes = sum(1 for row in shipped if row["check_exit"] != 0)
    reds = [row for row in rows if row["check_exit"] != 0]
    caught = sum(1 for row in reds if not ship(row))
    cost = sum(row["cost_usd"] for row in shipped)
    return {
        "ships": str(len(shipped)),
        "escapes": str(escapes),
        "reads": f"{opened}/{len(shipped)}",
        "catch": f"{caught}/{len(reds)}",
        "cost_usd": f"{cost:.2f}",
    }


def main() -> int:
    rows = json.loads((HERE / "sessions.json").read_text(encoding="utf-8"))
    before = measure(rows, ship_before)
    after = measure(rows, ship_after)
    print(f"before_ships {before['ships']}")
    print(f"before_escapes {before['escapes']}")
    print(f"before_reads {before['reads']}")
    print(f"before_catch {before['catch']}")
    print(f"before_cost_usd {before['cost_usd']}")
    print(f"after_ships {after['ships']}")
    print(f"after_escapes {after['escapes']}")
    print(f"after_reads {after['reads']}")
    print(f"after_catch {after['catch']}")
    print(f"after_cost_usd {after['cost_usd']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
