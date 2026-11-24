"""Starters miss the bug. Solutions catch it."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from mockagent.repo import dirty_src, make_repo  # noqa: E402

REVIEWS = ROOT / "labs" / "m01" / "fixtures" / "reviews.json"
BRIEF = ROOT / "briefs" / "gain-normalize" / "BRIEF.md"
VAGUE = ROOT / "labs" / "m02" / "fixtures" / "vague.md"


def run(script: Path, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *args],
        cwd=cwd or ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class Lab01(unittest.TestCase):
    def test_starter_ships_a_ticked_failure(self) -> None:
        proc = run(ROOT / "labs" / "m01" / "starter" / "review.py", str(REVIEWS))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("pr01 SHIP", proc.stdout)

    def test_solution_holds_the_same_failure_and_counts_reads(self) -> None:
        proc = run(ROOT / "labs" / "m01" / "solutions" / "review.py", str(REVIEWS))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("pr01 HOLD", proc.stdout)
        self.assertIn("pr04 SHIP", proc.stdout)
        self.assertIn("reads_per_ship=0.333", proc.stdout)
        records = json.loads(REVIEWS.read_text())
        shipped = [item for item in records if item["check_exit"] == 0]
        opened = sum(1 for item in shipped if item["human_opened"])
        self.assertEqual(f"{opened / len(shipped):.3f}", "0.333")


class Lab02(unittest.TestCase):
    def test_starter_accepts_the_vague_brief(self) -> None:
        proc = run(ROOT / "labs" / "m02" / "starter" / "brief_lint.py", str(VAGUE))
        self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_solution_rejects_the_vague_brief_and_accepts_the_real_one(self) -> None:
        bad = run(ROOT / "labs" / "m02" / "solutions" / "brief_lint.py", str(VAGUE))
        good = run(ROOT / "labs" / "m02" / "solutions" / "brief_lint.py", str(BRIEF))
        self.assertNotEqual(bad.returncode, 0, bad.stdout)
        self.assertIn("command:", bad.stdout)
        self.assertEqual(good.returncode, 0, good.stdout + good.stderr)


class Lab03(unittest.TestCase):
    def test_starter_ignores_a_harness_with_no_deny_rules(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / "harness", root / "proj", ignore=shutil.ignore_patterns("__pycache__"))
            settings = root / "proj" / ".claude" / "settings.json"
            body = json.loads(settings.read_text())
            body["permissions"]["deny"] = []
            settings.write_text(json.dumps(body))
            starter = run(ROOT / "labs" / "m03" / "starter" / "audit.py", str(root / "proj"))
            solution = run(ROOT / "labs" / "m03" / "solutions" / "audit.py", str(root / "proj"))
        self.assertEqual(starter.returncode, 0, starter.stdout)
        self.assertNotEqual(solution.returncode, 0, solution.stdout)
        self.assertIn("deny", solution.stdout)

    def test_solution_accepts_the_shipped_harness(self) -> None:
        proc = run(ROOT / "labs" / "m03" / "solutions" / "audit.py", str(ROOT / "harness"))
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


class Lab04(unittest.TestCase):
    def test_naive_stop_gate_trusts_a_touched_pass_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(Path(tmp), "failing")
            dirty_src(repo)
            evidence = repo / ".verify" / "evidence.md"
            evidence.write_text("VERDICT: PASS\n")
            newest = max(path.stat().st_mtime for path in repo.rglob("*") if path.is_file())
            os.utime(evidence, (newest + 10, newest + 10))
            naive = run(ROOT / "labs" / "m04" / "starter" / "stop_gate.py", str(repo))
            self.assertEqual(naive.returncode, 0, naive.stdout)
            self.assertIn("ALLOW", naive.stdout)
            env = os.environ.copy()
            env["PYTHONDONTWRITEBYTECODE"] = "1"
            env["VERIFY_STATE_DIR"] = str(Path(tmp) / "state")
            event = {
                "session_id": "naive-compare",
                "cwd": str(repo),
                "hook_event_name": "Stop",
                "stop_hook_active": False,
            }
            real = subprocess.run(
                [sys.executable, str(repo / ".claude" / "hooks" / "stop_gate.py")],
                input=json.dumps(event),
                text=True,
                capture_output=True,
                cwd=repo,
                env=env,
                check=False,
            )
        self.assertIn("code=BLOCK", real.stderr)
        self.assertIn('"decision": "block"', real.stdout)

    def test_naive_commit_gate_honors_a_substring(self) -> None:
        naive = run(
            ROOT / "labs" / "m04" / "starter" / "commit_gate.py",
            'echo Verified-by: none && git commit -m "ship"',
        )
        self.assertEqual(naive.returncode, 0)
        self.assertIn("ALLOW", naive.stdout)

    def test_weak_property_misses_the_withdrawal_bug(self) -> None:
        weak = run(ROOT / "labs" / "m04" / "starter" / "weak_property.py", "buggy")
        strong_bug = run(ROOT / "labs" / "m04" / "solutions" / "strong_property.py", "buggy")
        strong_fix = run(ROOT / "labs" / "m04" / "solutions" / "strong_property.py", "fixed")
        self.assertEqual(weak.returncode, 0)
        self.assertNotEqual(strong_bug.returncode, 0)
        self.assertEqual(strong_fix.returncode, 0)

    def test_repo_tries_file_resets_the_naive_counter_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = make_repo(Path(tmp), "failing")
            script = ROOT / "labs" / "m04" / "starter" / "stop_gate.py"
            self.assertEqual(run(script, str(repo)).returncode, 2)
            self.assertEqual(run(script, str(repo)).returncode, 2)
            (repo / ".verify" / ".tries").unlink()
            self.assertEqual(run(script, str(repo)).returncode, 2)


class CourseFiles(unittest.TestCase):
    def test_checks_match_the_commands_ci_runs(self) -> None:
        checks = json.loads((ROOT / "harness" / ".verify" / "checks.json").read_text())
        commands = {item["id"]: item["check"] for item in checks["checks"]}
        self.assertEqual(
            commands["pcmkit-unit"],
            "cargo test --manifest-path pcmkit/Cargo.toml --offline --workspace",
        )
        self.assertEqual(commands["pcmkit-oracle"], "python3 pcmkit/oracle/test_oracle.py")
        self.assertEqual(commands["pcmkit-cpp"], "bash pcmkit/cpp/run_consumer.sh")
        self.assertEqual(commands["harness-selftest"], "python3 -m unittest discover -s tests -v")
        self.assertEqual(commands["gain-normalize-accept"], "python3 briefs/gain-normalize/accept.py")

    def test_ruleset_requires_the_ci_jobs(self) -> None:
        ruleset = json.loads((ROOT / "harness" / ".github" / "ruleset.json").read_text())
        required = []
        for rule in ruleset["rules"]:
            if rule["type"] == "required_status_checks":
                required = [item["context"] for item in rule["parameters"]["required_status_checks"]]
        self.assertEqual(required, ["test", "site"])
        self.assertTrue(ruleset["rules"])
        self.assertIn("require_code_owner_review", json.dumps(ruleset))

    def test_skill_points_at_the_runner(self) -> None:
        text = (ROOT / "harness" / ".claude" / "skills" / "verify" / "SKILL.md").read_text()
        self.assertIn("python3 .verify/verify_runner.py", text)
        self.assertIn("name: verify", text)

    def test_no_api_keys_in_the_tree(self) -> None:
        banned = ("sk-" + "ant-", "sk-" + "proj-", "AK" + "IA", "BEGIN " + "PRIVATE KEY")
        allowed = {".py", ".md", ".json", ".rs", ".yml", ".yaml", ".toml", ".sh", ".cpp", ".h", ".mdc"}
        for path in ROOT.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in allowed:
                continue
            if any(part in path.parts for part in (".git", "target", "site", "__pycache__")):
                continue
            text = path.read_text(encoding="utf-8")
            for token in banned:
                self.assertNotIn(token, text, f"{token} in {path}")


if __name__ == "__main__":
    unittest.main()
