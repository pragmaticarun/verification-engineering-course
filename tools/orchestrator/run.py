#!/usr/bin/env python3
"""Put six mocked agents in git worktrees and admit only a fresh, green tree.

This process is the mock. A live orchestrator would be one agent process per
worktree. The decisions are the same ones: stale review hash, stale base,
failing check, or the merge queue. The budget is eight sessions. A ninth is
refused before any worktree is created.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

BUDGET = 8
HERE = Path(__file__).resolve().parent


def within_budget(count: int) -> bool:
    return count <= BUDGET


def decide(check_exit: int, tree_hash: str, reviewed_hash: str, head: str, reviewed_base: str) -> str:
    if reviewed_hash != tree_hash:
        return "stale"
    if reviewed_base != head:
        return "stale-base"
    if check_exit != 0:
        return "hold"
    return "queue"


def git(repo: Path, *args: str) -> str:
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = "Course"
    env["GIT_AUTHOR_EMAIL"] = "course@example.invalid"
    env["GIT_COMMITTER_NAME"] = "Course"
    env["GIT_COMMITTER_EMAIL"] = "course@example.invalid"
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        env=env,
    )
    return proc.stdout.strip()


def run_sessions(sessions: list[dict]) -> dict[str, int]:
    if not within_budget(len(sessions)):
        raise ValueError(f"budget is {BUDGET}")
    counts = {"sessions": len(sessions), "queued": 0, "held": 0, "stale": 0, "stale_base": 0, "worktrees": 0}
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / "repo"
        root.mkdir()
        git(root, "init", "-b", "main")
        (root / "README").write_text("base\n", encoding="utf-8")
        git(root, "add", "README")
        git(root, "commit", "-m", "base")
        head = git(root, "rev-parse", "HEAD")
        for session in sessions:
            worktree = Path(tmp) / session["id"]
            git(root, "worktree", "add", "-b", session["id"], str(worktree))
            counts["worktrees"] += 1
            (worktree / "change.txt").write_text(session["body"], encoding="utf-8")
            tree_hash = hashlib.sha256(session["body"].encode("utf-8")).hexdigest()
            reviewed_hash = tree_hash if session["reviewed_hash"] == "MATCH" else "0" * 64
            reviewed_base = head if session["reviewed_base"] == "HEAD" else "0" * 40
            decision = decide(session["check_exit"], tree_hash, reviewed_hash, head, reviewed_base)
            if decision == "queue":
                counts["queued"] += 1
            elif decision == "hold":
                counts["held"] += 1
            elif decision == "stale":
                counts["stale"] += 1
            elif decision == "stale-base":
                counts["stale_base"] += 1
    return counts


def main() -> int:
    sessions = json.loads((HERE / "sessions.json").read_text(encoding="utf-8"))
    counts = run_sessions(sessions)
    print(f"sessions {counts['sessions']}")
    print(f"worktrees {counts['worktrees']}")
    print(f"queued {counts['queued']}")
    print(f"held {counts['held']}")
    print(f"stale {counts['stale']}")
    print(f"stale_base {counts['stale_base']}")
    print(f"budget {BUDGET}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
