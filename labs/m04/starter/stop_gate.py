#!/usr/bin/env python3
"""Naive stop gate.

A PASS line in a file the agent can write, plus a newer mtime, is treated as
proof. The retry counter lives in the repository, so it is one counter for
every session and the agent can delete it.
"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    evidence = repo / ".verify" / "evidence.md"
    tries = repo / ".verify" / ".tries"
    text = evidence.read_text() if evidence.exists() else ""
    newest = 0.0
    for path in repo.rglob("*"):
        if not path.is_file() or path == evidence or ".git" in path.parts:
            continue
        newest = max(newest, path.stat().st_mtime)
    fresh = evidence.exists() and evidence.stat().st_mtime >= newest
    if "VERDICT: PASS" in text and fresh:
        print("ALLOW")
        return 0
    count = int(tries.read_text()) if tries.exists() else 0
    count += 1
    tries.parent.mkdir(parents=True, exist_ok=True)
    tries.write_text(str(count))
    if count >= 3:
        print("ALLOW")
        return 0
    print("BLOCK")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
