#!/usr/bin/env python3
"""Claude Code Stop and SubagentStop hook.

Reads the documented hook event on stdin and prints a Stop decision on stdout.
Exit 0 with a JSON ``decision: block`` keeps the agent working. Empty stdout
lets the turn end. The verdict comes from running checks, not from a file the
agent wrote.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".verify"))

from lib.engine import decide_stop, render_stop  # noqa: E402


def main() -> int:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw) if raw.strip() else {"_invalid": True}
    except json.JSONDecodeError:
        event = {"_invalid": True, "hook_event_name": "Stop"}
    if not isinstance(event, dict):
        event = {"_invalid": True, "hook_event_name": "Stop"}
    repo = Path(str(event.get("cwd") or ".")).resolve()
    decision = decide_stop(event, repo)
    sys.stdout.write(render_stop(decision))
    print(f"VERIFY code={decision.code} allow={str(decision.allow).lower()}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
