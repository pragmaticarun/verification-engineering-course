#!/usr/bin/env python3
"""Run the held-out peak cases the visible suite does not contain.

The visible cases are all >= 0. A peak that is `max(samples)` passes them and
fails the hidden file. CI runs this script. The mock-agent worktree does not
copy `tools/heldout/`.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from peak import peak, peak_visible_only

HERE = Path(__file__).resolve().parent


def load(name: str) -> list[dict]:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def misses(fn, cases: list[dict]) -> list[str]:
    bad = []
    for case in cases:
        if fn(case["samples"]) != case["peak"]:
            bad.append(case["id"])
    return bad


def main() -> int:
    visible = load("visible_cases.json")
    hidden = load("hidden_cases.json")
    if misses(peak, visible) or misses(peak, hidden):
        print("held-out failed", file=sys.stderr)
        return 1
    visible_gap = misses(peak_visible_only, visible)
    hidden_gap = misses(peak_visible_only, hidden)
    if visible_gap or not hidden_gap:
        print("visible-only gap disappeared", file=sys.stderr)
        return 1
    print(f"held-out ok {len(hidden)}")
    print(f"visible-only missed {len(hidden_gap)}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(HERE))
    raise SystemExit(main())
