"""Starters for modules 5–12 and the capstone miss the bug. Solutions catch it."""

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


class Lab09(unittest.TestCase):
    def test_visible_cases_hide_a_negative_peak(self) -> None:
        visible = ROOT / "tools" / "heldout" / "visible_cases.json"
        hidden = ROOT / "tools" / "heldout" / "hidden_cases.json"
        starter = ROOT / "labs" / "m09" / "starter" / "peak.py"
        solution = ROOT / "labs" / "m09" / "solutions" / "peak.py"
        self.assertEqual(run(starter, str(visible)).returncode, 0)
        self.assertNotEqual(run(starter, str(hidden)).returncode, 0)
        self.assertEqual(run(solution, str(visible)).returncode, 0)
        self.assertEqual(run(solution, str(hidden)).returncode, 0)

    def test_held_out_runner_and_codeowners_template(self) -> None:
        proc = run(ROOT / "tools" / "heldout" / "run.py")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, (ROOT / "tools" / "heldout" / "expected.txt").read_text())
        owners = (ROOT / "harness" / "platform" / "CODEOWNERS").read_text()
        self.assertIn("/.verify/", owners)
        self.assertIn("/tools/heldout/", owners)
        self.assertIn("/pcmkit/", owners)


class Lab10(unittest.TestCase):
    def test_word_bug_is_not_a_rubric(self) -> None:
        reviews = ROOT / "tools" / "reviewer" / "reviews.json"
        starter = run(ROOT / "labs" / "m10" / "starter" / "decide.py", str(reviews))
        solution = run(ROOT / "labs" / "m10" / "solutions" / "decide.py", str(reviews))
        scored = run(ROOT / "tools" / "reviewer" / "score.py")
        self.assertNotEqual(starter.returncode, 0)
        self.assertEqual(solution.returncode, 0, solution.stdout + solution.stderr)
        self.assertEqual(scored.returncode, 0, scored.stderr)
        self.assertEqual(scored.stdout, (ROOT / "tools" / "reviewer" / "expected.txt").read_text())
        self.assertIn("tune_excluded 4", scored.stdout)
        self.assertIn("adversary_rejected 1", scored.stdout)


class Lab11(unittest.TestCase):
    def test_stale_review_is_not_admitted(self) -> None:
        sessions = ROOT / "labs" / "m11" / "fixtures" / "sessions.json"
        starter = run(ROOT / "labs" / "m11" / "starter" / "admit.py", str(sessions))
        solution = run(ROOT / "labs" / "m11" / "solutions" / "admit.py", str(sessions))
        self.assertNotEqual(starter.returncode, 0)
        self.assertEqual(solution.returncode, 0, solution.stdout + solution.stderr)

    def test_six_worktrees_and_a_budget(self) -> None:
        proc = run(ROOT / "tools" / "orchestrator" / "run.py")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout, (ROOT / "tools" / "orchestrator" / "expected.txt").read_text())
        self.assertIn("worktrees 6", proc.stdout)
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "course_orchestrator", ROOT / "tools" / "orchestrator" / "run.py"
        )
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertFalse(module.within_budget(9))
        with self.assertRaises(ValueError):
            module.run_sessions([{"id": f"x{i}"} for i in range(9)])


class Lab12(unittest.TestCase):
    def test_quiet_is_not_a_reason_to_drop_tamper(self) -> None:
        checks = ROOT / "labs" / "m12" / "fixtures" / "checks.json"
        starter = run(ROOT / "labs" / "m12" / "starter" / "prune.py", str(checks))
        solution = run(ROOT / "labs" / "m12" / "solutions" / "prune.py", str(checks))
        report = run(ROOT / "tools" / "metrics" / "report.py")
        self.assertNotEqual(starter.returncode, 0)
        self.assertEqual(solution.returncode, 0, solution.stdout + solution.stderr)
        self.assertEqual(report.returncode, 0, report.stderr)
        self.assertEqual(report.stdout, (ROOT / "tools" / "metrics" / "expected.txt").read_text())
        self.assertIn("kept held-out,tamper", report.stdout)


class LabCapstone(unittest.TestCase):
    def test_ticks_ship_a_red_check_and_the_exit_code_does_not(self) -> None:
        sessions = ROOT / "tools" / "capstone" / "sessions.json"
        starter = run(ROOT / "labs" / "capstone" / "starter" / "policy.py", str(sessions))
        solution = run(ROOT / "labs" / "capstone" / "solutions" / "policy.py", str(sessions))
        measured = run(ROOT / "tools" / "capstone" / "before_after.py")
        self.assertNotEqual(starter.returncode, 0)
        self.assertEqual(solution.returncode, 0, solution.stdout + solution.stderr)
        self.assertEqual(measured.returncode, 0, measured.stderr)
        self.assertEqual(measured.stdout, (ROOT / "tools" / "capstone" / "expected.txt").read_text())
        self.assertIn("after_escapes 0", measured.stdout)
        self.assertIn("before_escapes 3", measured.stdout)


if __name__ == "__main__":
    unittest.main()
