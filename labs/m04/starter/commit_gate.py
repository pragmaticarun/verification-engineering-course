#!/usr/bin/env python3
"""Naive commit gate: the exemption string anywhere in the command is enough."""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    command = sys.argv[1]
    repo = Path(sys.argv[2] if len(sys.argv) > 2 else ".").resolve()
    if "Verified-by: none" in command:
        print("ALLOW")
        return 0
    evidence = repo / ".verify" / "evidence.md"
    if evidence.exists() and "VERDICT: PASS" in evidence.read_text():
        print("ALLOW")
        return 0
    print("BLOCK")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
