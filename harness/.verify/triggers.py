#!/usr/bin/env python3
"""List checks the current diff triggers, and fail closed on structural problems.

This does not run the checks. `verify_runner.py` runs them. A missing checks
file on the base ref is a failure, not an empty trigger list.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.engine import structural_problems  # noqa: E402


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    problems, triggered = structural_problems(repo)
    for check_id in triggered:
        print(f"triggered: {check_id}")
    if problems:
        for problem in problems:
            print(f"PROBLEM: {problem}")
        return 1
    if not triggered:
        print("triggered: (none)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
