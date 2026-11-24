#!/usr/bin/env python3
"""Reject sleeps, skips, and a retry loop in the fast tier.

The scanner looks for the call, not the English word. A comment that names
the policy is fine. A test that sleeps until it passes is not.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = (
    re.compile(r"\btime\.sleep\s*\("),
    re.compile(r"\bthread::sleep"),
    re.compile(r"\bthis_thread::sleep"),
    re.compile(r"pytest\.mark\.flaky"),
    re.compile(r"pytest\.mark\.skip"),
    re.compile(r"\bpytest\.skip\s*\("),
    re.compile(r"@unittest\.skip"),
    re.compile(r"#\[ignore\]"),
    re.compile("retry-" + "until-green"),
)

SUFFIXES = {".py", ".rs", ".cpp", ".h", ".hpp"}


def scan(root: Path) -> list[str]:
    problems: list[str] = []
    files = [root] if root.is_file() else sorted(path for path in root.rglob("*") if path.is_file())
    for path in files:
        if path.suffix not in SUFFIXES:
            continue
        if any(part in path.parts for part in ("target", "build", "build-san", "__pycache__")):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for number, line in enumerate(text.splitlines(), start=1):
            if any(pattern.search(line) for pattern in PATTERNS):
                problems.append(f"{path}:{number}: {line.strip()}")
    return problems


def main() -> int:
    roots = [Path(arg) for arg in sys.argv[1:]] or [Path("pcmkit"), Path("briefs")]
    problems: list[str] = []
    for root in roots:
        problems.extend(scan(root))
    if problems:
        print("\n".join(problems))
        return 1
    print("flaky-scan ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
