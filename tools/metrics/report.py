#!/usr/bin/env python3
"""Metrics for one recorded week, and a pruner that will not drop a quiet lock.

The 60-day figure is the source article's prune window. It is not a result
from this repo. A check marked catastrophic stays even when it has been quiet
longer than that window. Quiet here means days since it last failed a change.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

QUIET_DAYS = 60
HERE = Path(__file__).resolve().parent


def median(values: list[int]) -> str:
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2 == 1:
        return str(ordered[mid])
    left = ordered[mid - 1]
    right = ordered[mid]
    if (left + right) % 2 == 0:
        return str((left + right) // 2)
    return f"{(left + right) / 2:.1f}"


def money(amount: float) -> str:
    return f"{amount:.2f}"


def summarize(runs: list[dict]) -> dict[str, str]:
    ships = [row for row in runs if row["merged"]]
    opened = sum(1 for row in ships if row["human_opened"])
    escapes = sum(1 for row in ships if row["escaped"])
    reds = [row for row in runs if row["check_exit"] != 0]
    caught = sum(1 for row in reds if not row["merged"])
    holds = [row for row in runs if row["false_hold"] or (not row["merged"] and row["check_exit"] != 0)]
    false_holds = sum(1 for row in holds if row["false_hold"])
    return {
        "ships": str(len(ships)),
        "reads_per_ship": f"{opened}/{len(ships)}",
        "escapes": str(escapes),
        "cost_usd": money(sum(row["cost_usd"] for row in runs)),
        "median_minutes": median([row["minutes"] for row in ships]),
        "false_hold_rate": f"{false_holds}/{len(holds)}",
        "catch_rate": f"{caught}/{len(reds)}",
    }


def prune(checks: list[dict]) -> tuple[list[str], list[str]]:
    kept: list[str] = []
    dropped: list[str] = []
    for check in checks:
        if check["days_quiet"] >= QUIET_DAYS and not check["catastrophic"]:
            dropped.append(check["id"])
        else:
            kept.append(check["id"])
    return kept, dropped


def main() -> int:
    runs = json.loads((HERE / "runs.json").read_text(encoding="utf-8"))
    checks = json.loads((HERE / "checks.json").read_text(encoding="utf-8"))
    summary = summarize(runs)
    kept, dropped = prune(checks)
    if "tamper" not in kept:
        print("pruner dropped a catastrophic check", file=sys.stderr)
        return 1
    print(f"ships {summary['ships']}")
    print(f"reads_per_ship {summary['reads_per_ship']}")
    print(f"escapes {summary['escapes']}")
    print(f"cost_usd {summary['cost_usd']}")
    print(f"median_minutes {summary['median_minutes']}")
    print(f"false_hold_rate {summary['false_hold_rate']}")
    print(f"catch_rate {summary['catch_rate']}")
    print(f"pruned {','.join(dropped)}")
    print(f"kept {','.join(sorted(kept))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
