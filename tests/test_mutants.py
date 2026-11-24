"""The mutants allowlist reads missed.txt, not the colored log line."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools" / "heavy"))

import mutant_report  # noqa: E402


FIXTURE = ROOT / "tools" / "heavy" / "fixtures" / "missed.txt"

# The bytes GitHub Actions printed for run 45410288766, before the script
# rejected them. Color wraps MISSED and the operators.
COLORED = (
    "\x1b[31m\x1b[1mMISSED  \x1b[0m crates/pcmkit/src/clamp.rs:19:15: "
    "replace \x1b[33m>\x1b[0m with \x1b[38;5;11m>=\x1b[0m in "
    "\x1b[38;5;13mclamp_unit\x1b[0m in \x1b[36m0s\x1b[0m \x1b[2mbuild\x1b[0m + "
    "\x1b[36m0s\x1b[0m \x1b[2mtest\x1b[0m\n"
    "\x1b[31m\x1b[1mMISSED  \x1b[0m crates/pcmkit/src/clamp.rs:21:22: "
    "replace \x1b[33m<\x1b[0m with \x1b[38;5;11m<=\x1b[0m in "
    "\x1b[38;5;13mclamp_unit\x1b[0m in \x1b[36m0s\x1b[0m \x1b[2mbuild\x1b[0m + "
    "\x1b[36m0s\x1b[0m \x1b[2mtest\x1b[0m\n"
)


class MutantAllowlist(unittest.TestCase):
    def test_recorded_missed_txt_is_the_two_equivalent_edits(self) -> None:
        problems = mutant_report.compare_misses(FIXTURE.read_text(encoding="utf-8"))
        self.assertEqual(problems, [])

    def test_colored_log_lines_match_the_same_allowlist(self) -> None:
        problems = mutant_report.compare_misses(COLORED)
        self.assertEqual(problems, [])

    def test_column_is_not_part_of_the_allowlist(self) -> None:
        shifted = FIXTURE.read_text(encoding="utf-8").replace(":19:15:", ":19:99:").replace(":21:22:", ":21:3:")
        self.assertEqual(mutant_report.compare_misses(shifted), [])

    def test_a_third_miss_is_rejected(self) -> None:
        extra = FIXTURE.read_text(encoding="utf-8") + "crates/pcmkit/src/clamp.rs:19:15: replace > with < in clamp_unit\n"
        problems = mutant_report.compare_misses(extra)
        self.assertEqual(len(problems), 1)
        self.assertIn("unexpected misses:", problems[0])
        self.assertIn("replace > with < in clamp_unit", problems[0])

    def test_caught_txt_counts_nonempty_lines(self) -> None:
        self.assertEqual(mutant_report.caught_count("a\n\nb\n"), 2)


if __name__ == "__main__":
    unittest.main()
