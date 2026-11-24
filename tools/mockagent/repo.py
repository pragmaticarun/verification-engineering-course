"""Build a tiny git repository around a copy of the harness."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

COURSE = Path(__file__).resolve().parents[2]
HARNESS = COURSE / "harness"

SCOPED_BRIEF = """# Brief: touch the library

## Goal
Change the library constant and nothing else.

## Acceptance
command: python3 smoke.py
expect_exit: 0

## Non-goals
- Editing the harness
- Adding a second module

## Allowed-files
- src/lib.py
"""


def git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        capture_output=True,
        text=True,
    )


def make_repo(tmp: Path, profile: str = "passing") -> Path:
    repo = tmp / "repo"
    if repo.exists():
        shutil.rmtree(repo)
    shutil.copytree(
        HARNESS,
        repo,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "evidence.json", "evidence.md"),
    )
    gate = {"mode": "enforce", "max_stop_rounds": 2, "platform_continuation_cap": 8}
    smoke_exit = 0
    if profile == "failing":
        smoke_exit = 1
    elif profile == "observe":
        gate["mode"] = "observe"
        smoke_exit = 1
    elif profile == "off":
        gate["mode"] = "off"
        smoke_exit = 1
    elif profile == "cap":
        gate["max_stop_rounds"] = 100
        smoke_exit = 1
    elif profile == "scoped":
        smoke_exit = 0
    (repo / ".verify" / "gate.json").write_text(json.dumps(gate) + "\n")
    command = "python3 smoke.py"
    checks = {
        "locked": [],
        "test_paths": ["**/*_test.py", "**/test_*.py"],
        "checks": [
            {
                "id": "smoke",
                "when": ["src/**"],
                "check": command,
                "why": "Fixture command so the hook runs a real process.",
            }
        ],
    }
    (repo / "smoke.py").write_text(f"import sys\nsys.exit({smoke_exit})\n")
    (repo / "src").mkdir(exist_ok=True)
    (repo / "src" / "lib.py").write_text("VALUE = 1\n")
    (repo / "sample_test.py").write_text("def test_ok():\n    assert True\n")
    if profile == "scoped":
        brief_dir = repo / "briefs" / "task"
        brief_dir.mkdir(parents=True)
        (brief_dir / "BRIEF.md").write_text(SCOPED_BRIEF)
        (repo / ".verify" / "active-brief").write_text("briefs/task/BRIEF.md\n")
    if profile == "no-checks":
        (repo / ".verify" / "checks.json").unlink()
    else:
        (repo / ".verify" / "checks.json").write_text(json.dumps(checks) + "\n")
    subprocess.run(["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True)
    git(repo, "config", "user.email", "course@example.com")
    git(repo, "config", "user.name", "Course Fixture")
    git(repo, "add", "-A")
    git(repo, "commit", "-m", "base")
    if profile == "no-checks":
        passing = dict(checks)
        passing["checks"][0]["check"] = "python3 -c \"import sys; sys.exit(0)\""
        (repo / ".verify" / "checks.json").write_text(json.dumps(passing) + "\n")
        (repo / "src" / "lib.py").write_text("VALUE = 2\n")
    return repo


def dirty_src(repo: Path, text: str = "VALUE = 2\n") -> None:
    (repo / "src" / "lib.py").write_text(text)


def load_event(name: str, repo: Path, session: str, **overrides) -> dict:
    event = json.loads((COURSE / "scenarios" / "events" / name).read_text())
    event["cwd"] = str(repo)
    event["session_id"] = session
    event.update(overrides)
    return event


def run_script(repo: Path, script: str, event: dict, state: Path, env_extra: dict | None = None):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["VERIFY_STATE_DIR"] = str(state)
    env.pop("VERIFY_BASE_REF", None)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [os.environ.get("PYTHON", "python3"), str(repo / script)],
        input=json.dumps(event),
        text=True,
        capture_output=True,
        cwd=repo,
        env=env,
        check=False,
    )


def verify_line(stderr: str) -> tuple[str, bool]:
    for line in stderr.splitlines():
        if line.startswith("VERIFY "):
            fields = dict(part.split("=", 1) for part in line.split()[1:])
            return fields["code"], fields["allow"] == "true"
    raise AssertionError(f"no VERIFY line in stderr:\n{stderr}")
