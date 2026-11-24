#!/usr/bin/env python3
"""Run the base-branch checks and write evidence.json.

Evidence is a record of commands that ran. It is not a note the agent authors.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.engine import audit_evidence_file, run_verify  # noqa: E402


def main() -> int:
    positional = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
    repo = Path(positional[0] if positional else ".").resolve()
    report = run_verify(repo)
    print(f"VERDICT: {report.verdict}")
    print(f"TREE: {report.tree_hash}")
    for problem in report.problems:
        print(f"PROBLEM: {problem}")
    if "--audit" in sys.argv:
        for problem in audit_evidence_file(repo):
            print(f"AUDIT: {problem}")
            return 1
    return 0 if report.verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
