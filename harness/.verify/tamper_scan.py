#!/usr/bin/env python3
"""Flag diffs that skip a test or special-case the test name.

Heuristics, not a proof. CI still re-runs the suite. The patterns are the
ones a patch uses when it wants a green run without the behavior.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.engine import tamper_problems  # noqa: E402


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    problems = tamper_problems(repo)
    if not problems:
        print("tamper: none")
        return 0
    for problem in problems:
        print(f"PROBLEM: {problem}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
