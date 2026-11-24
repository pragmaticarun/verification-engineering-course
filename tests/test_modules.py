"""Starters for modules 5–8 miss the bug. Solutions catch it."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class Lab05(unittest.TestCase):
    def test_starter_accepts_same_length_and_solution_rejects_it(self) -> None:
        left = ROOT / "labs" / "m05" / "fixtures" / "left.bin"
        right = ROOT / "labs" / "m05" / "fixtures" / "right.bin"
        starter = run(ROOT / "labs" / "m05" / "starter" / "compare.py", str(left), str(right))
        solution = run(ROOT / "labs" / "m05" / "solutions" / "compare.py", str(left), str(right))
        self.assertEqual(starter.returncode, 0, starter.stderr)
        self.assertNotEqual(solution.returncode, 0, solution.stdout)

    def test_flaky_scan_rejects_a_sleep(self) -> None:
        proc = run(ROOT / "pcmkit" / "fast" / "flaky_scan.py", str(ROOT / "labs" / "m05" / "fixtures" / "sleepy.py"))
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("time.sleep", proc.stdout)


class Lab06(unittest.TestCase):
    def test_weak_property_accepts_the_mutant(self) -> None:
        starter = run(ROOT / "labs" / "m06" / "starter" / "property.py", "mutant")
        solution = run(ROOT / "labs" / "m06" / "solutions" / "property.py", "mutant")
        correct = run(ROOT / "labs" / "m06" / "solutions" / "property.py", "correct")
        self.assertEqual(starter.returncode, 0, starter.stderr)
        self.assertNotEqual(solution.returncode, 0)
        self.assertEqual(correct.returncode, 0, correct.stdout + correct.stderr)


class Lab07(unittest.TestCase):
    def test_one_sample_is_not_a_range_proof(self) -> None:
        starter = run(ROOT / "labs" / "m07" / "starter" / "range_check.py", "broken")
        solution = run(ROOT / "labs" / "m07" / "solutions" / "range_check.py", "broken")
        clamped = run(ROOT / "labs" / "m07" / "solutions" / "range_check.py", "clamped")
        self.assertEqual(starter.returncode, 0, starter.stderr)
        self.assertNotEqual(solution.returncode, 0)
        self.assertEqual(clamped.returncode, 0, clamped.stdout + clamped.stderr)


class Lab08(unittest.TestCase):
    def test_a_listening_bluff_is_not_an_e2e_result(self) -> None:
        honest = ROOT / "labs" / "m08" / "fixtures" / "honest.txt"
        bluff = ROOT / "labs" / "m08" / "fixtures" / "bluff.txt"
        starter = run(ROOT / "labs" / "m08" / "starter" / "narrate.py", str(bluff))
        solution_bluff = run(ROOT / "labs" / "m08" / "solutions" / "narrate.py", str(bluff))
        solution_honest = run(ROOT / "labs" / "m08" / "solutions" / "narrate.py", str(honest))
        self.assertEqual(starter.returncode, 0, starter.stderr)
        self.assertNotEqual(solution_bluff.returncode, 0)
        self.assertEqual(solution_honest.returncode, 0, solution_honest.stdout + solution_honest.stderr)


if __name__ == "__main__":
    unittest.main()
