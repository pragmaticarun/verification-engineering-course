#!/usr/bin/env python3
"""The property that only deposits, so a missing withdrawal still looks fine."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ledger import buggy, fixed  # noqa: E402


def holds(balance_fn) -> bool:
    for amount in (0, 1, 5, 10):
        if balance_fn([("deposit", amount)]) < 0:
            return False
    return True


def main() -> int:
    name = sys.argv[1] if len(sys.argv) > 1 else "buggy"
    fn = buggy if name == "buggy" else fixed
    if holds(fn):
        print("holds")
        return 0
    print("fails")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
