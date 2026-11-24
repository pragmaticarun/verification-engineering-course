#!/usr/bin/env python3
"""Compare cargo-mutants misses to the two equivalent clamp mutants.

The allowlist is file, line, and mutation text. Column, color, a leading
MISSED word, and the timing suffix are not part of the comparison. GitHub
Actions paints the log, so reading mutants.out/missed.txt is the source of
truth. The same parser accepts a colored log line, which is what the unit
test locks.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ANSI = re.compile(r"\x1b\[[0-9;]*m")
TIMING = re.compile(r"\s+in\s+\d+s\s+build\s+\+\s+\d+s\s+test\s*$")
MISS = re.compile(r"^(?P<file>.+?):(?P<line>\d+):(?P<col>\d+):\s*(?P<mutation>.+)$")

# Equivalent edits: the sample that is already on the rail takes the same path.
EXPECTED = (
    ("crates/pcmkit/src/clamp.rs", 19, "replace > with >= in clamp_unit"),
    ("crates/pcmkit/src/clamp.rs", 21, "replace < with <= in clamp_unit"),
)
CAUGHT = 9


def strip_ansi(text: str) -> str:
    return ANSI.sub("", text)


def parse_misses(text: str) -> tuple[list[tuple[str, int, str]], list[str]]:
    found: list[tuple[str, int, str]] = []
    problems: list[str] = []
    for raw in text.splitlines():
        clean = TIMING.sub("", strip_ansi(raw)).strip()
        if not clean:
            continue
        clean = re.sub(r"^MISSED\s+", "", clean)
        match = MISS.fullmatch(clean)
        if not match:
            problems.append(f"unparsed: {clean}")
            continue
        found.append((match.group("file"), int(match.group("line")), match.group("mutation").strip()))
    return found, problems


def compare_misses(
    text: str,
    expected: tuple[tuple[str, int, str], ...] = EXPECTED,
) -> list[str]:
    """Problems with this miss report. An empty list means it is the allowlist."""
    found, problems = parse_misses(text)
    if problems:
        return problems
    if sorted(found) != sorted(expected):
        rendered = "\n".join(f"{path}:{line}: {mutation}" for path, line, mutation in found)
        wanted = "\n".join(f"{path}:{line}: {mutation}" for path, line, mutation in expected)
        return [f"unexpected misses:\n{rendered}\nexpected:\n{wanted}"]
    return []


def caught_count(text: str) -> int:
    return sum(1 for line in text.splitlines() if line.strip())


def main() -> int:
    missed_path, caught_path, code = sys.argv[1:]
    if int(code) != 2:
        print(f"cargo-mutants exit {code}, expected 2 for the two equivalent mutants", file=sys.stderr)
        return 1
    missed_file = Path(missed_path)
    caught_file = Path(caught_path)
    if not missed_file.is_file() or not caught_file.is_file():
        print(f"missing mutants report under {missed_file.parent}", file=sys.stderr)
        return 1
    problems = compare_misses(missed_file.read_text(encoding="utf-8"))
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    caught = caught_count(caught_file.read_text(encoding="utf-8"))
    if caught != CAUGHT:
        print(f"caught {caught}, expected {CAUGHT}", file=sys.stderr)
        return 1
    print(f"mutants smoke ok: {CAUGHT} caught, 2 equivalent misses")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
