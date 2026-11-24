#!/usr/bin/env python3
"""Claude Code PreToolUse hook for Bash.

A `git commit` is denied unless the base-branch checks have just passed, or
the message carries `Verified-by: none` as a real trailer plus a substantive
`Exemption-reason`. Finding that phrase anywhere else in the command is not
an exemption. The hook answers with PreToolUse `permissionDecision` JSON.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".verify"))

from lib.engine import decide_commit, render_commit  # noqa: E402


def main() -> int:
    raw = sys.stdin.read()
    try:
        event = json.loads(raw) if raw.strip() else {"_invalid": True}
    except json.JSONDecodeError:
        event = {"_invalid": True, "hook_event_name": "PreToolUse", "tool_name": "Bash"}
    if not isinstance(event, dict):
        event = {"_invalid": True, "hook_event_name": "PreToolUse", "tool_name": "Bash"}
    repo = Path(str(event.get("cwd") or ".")).resolve()
    decision = decide_commit(event, repo)
    sys.stdout.write(render_commit(decision))
    print(f"VERIFY code={decision.code} allow={str(decision.allow).lower()}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
