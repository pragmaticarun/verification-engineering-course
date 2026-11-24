#!/usr/bin/env python3
"""A ledger property that deposits, withdraws, and rejects an overdraft."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ledger import buggy, fixed  # noqa: E402


def holds(balance_fn) -> bool:
    if balance_fn([]) != 0:
        return False
    if balance_fn([("deposit", 5), ("withdraw", 5)]) != 0:
        return False
    if balance_fn([("deposit", 5), ("withdraw", 6)]) != 5:
        return False
    if balance_fn([("withdraw", 1)]) != 0:
        return False
    if balance_fn([("deposit", 3), ("deposit", 4), ("withdraw", 2)]) != 5:
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
