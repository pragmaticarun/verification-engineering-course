#!/usr/bin/env python3
"""Solution: a review counts only for the tree hash it names."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def admit(session: dict) -> bool:
    return session["tree_hash"] == session["reviewed_hash"]


def main() -> int:
    sessions = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    for session in sessions:
        fresh = session["tree_hash"] == session["reviewed_hash"]
        if admit(session) and not fresh:
            print(f"admitted stale {session['id']}")
            return 1
        if fresh and not admit(session):
            print(f"rejected fresh {session['id']}")
            return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
