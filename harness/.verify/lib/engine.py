"""Decisions for the stop gate and the commit gate.

The agent does not get to grade itself. A stop or a commit is allowed when
commands from the base-branch checks file have just been executed, or when a
parsed exemption trailer carries a real reason. A PASS line in a file, a
touched mtime, and the substring ``Verified-by: none`` are not evidence.

Local hooks are still not the lock. They do not run for a human's own git,
and the copy of this file in the worktree is the copy that runs. The lock is
CI on a protected branch, which re-runs the same functions on the base
version of the harness. See the ruleset template next to this tree.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from .brief import allowed_globs

MINIMUM_LOCK = (
    ".claude/settings.json",
    ".claude/hooks/",
    ".claude/skills/",
    ".verify/checks.json",
    ".verify/gate.json",
    ".verify/verify_runner.py",
    ".verify/triggers.py",
    ".verify/tamper_scan.py",
    ".verify/lib/",
    ".verify/active-brief",
    "AGENTS.md",
    "CLAUDE.md",
    "REVIEW.md",
    ".cursor/rules/",
)

DEFAULT_TEST_PATHS = (
    "**/tests/**",
    "**/*_test.rs",
    "**/test_*.py",
    "**/*_test.py",
    "**/tests.rs",
)

HASH_SKIP_DIRS = {".git", "target", "__pycache__", ".venv", "site", "build", ".cache"}
HASH_SKIP_FILES = {
    ".verify/evidence.json",
    ".verify/evidence.md",
    ".verify/NEEDS-HUMAN.md",
}
SOURCE_SUFFIXES = {".rs", ".py", ".cpp", ".h", ".hpp", ".c", ".cc"}
WEAK_REASONS = {
    "",
    "none",
    "n/a",
    "na",
    "todo",
    "later",
    "test",
    "fix",
    "wip",
    "because",
    "yes",
    "ok",
    "okay",
    "ship it",
}


@dataclass
class Decision:
    allow: bool
    code: str
    message: str


@dataclass
class Report:
    verdict: str
    problems: list[str]
    tree_hash: str
    commands: list[dict]
    triggered: list[str]
    changed: list[str] = field(default_factory=list)

    def to_evidence(self) -> dict:
        body = {
            "schema": 1,
            "produced_by": "verify_runner",
            "tree_hash": self.tree_hash,
            "verdict": self.verdict,
            "problems": self.problems,
            "commands": self.commands,
            "triggered": self.triggered,
            "tool_versions": {"python": platform.python_version()},
            "finished_at": datetime.now(timezone.utc).isoformat(),
        }
        body["integrity"] = integrity(body)
        return body


def integrity(body: dict) -> str:
    payload = {key: body[key] for key in ("commands", "problems", "produced_by", "tree_hash", "verdict")}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def glob_match(pattern: str, path: str) -> bool:
    path = path.replace("\\", "/")
    pattern = pattern.replace("\\", "/")
    regex: list[str] = []
    index = 0
    while index < len(pattern):
        if pattern.startswith("**/", index):
            regex.append("(?:.*/)?")
            index += 3
        elif pattern.startswith("**", index):
            regex.append(".*")
            index += 2
        elif pattern[index] == "*":
            regex.append("[^/]*")
            index += 1
        elif pattern[index] == "?":
            regex.append("[^/]")
            index += 1
        else:
            regex.append(re.escape(pattern[index]))
            index += 1
    return re.fullmatch("".join(regex), path) is not None


def is_locked(path: str, patterns: list[str]) -> bool:
    path = path.replace("\\", "/")
    for entry in patterns:
        entry = entry.replace("\\", "/")
        if entry.endswith("/"):
            prefix = entry
            if path.startswith(prefix) or path == prefix.rstrip("/"):
                return True
        elif path == entry or glob_match(entry, path):
            return True
    return False


def strong_reason(value: str) -> bool:
    text = " ".join(value.strip().split())
    if len(text) < 20:
        return False
    if text.lower() in WEAK_REASONS:
        return False
    return True


def git(repo: Path, *args: str, check: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=check,
        capture_output=True,
        text=True,
    )


def base_ref(repo: Path) -> str | None:
    override = os.environ.get("VERIFY_BASE_REF")
    if override:
        return override
    for candidate in ("origin/main", "main"):
        proc = git(repo, "rev-parse", "--verify", "--quiet", candidate)
        if proc.returncode == 0 and proc.stdout.strip():
            return candidate
    return None


def read_base_text(repo: Path, rel: str) -> str | None:
    ref = base_ref(repo)
    if ref is None:
        return None
    proc = git(repo, "show", f"{ref}:{rel}")
    if proc.returncode != 0:
        return None
    return proc.stdout


def read_gate(repo: Path) -> dict:
    fallback = {
        "mode": "enforce",
        "max_stop_rounds": 2,
        "platform_continuation_cap": 8,
        "source": "fail-closed",
    }
    text = read_base_text(repo, ".verify/gate.json")
    if text is None:
        return fallback
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        fallback["source"] = "invalid"
        return fallback
    mode = data.get("mode", "enforce")
    if mode not in ("off", "observe", "enforce"):
        mode = "enforce"
    data["mode"] = mode
    data.setdefault("max_stop_rounds", 2)
    data.setdefault("platform_continuation_cap", 8)
    data["source"] = "base"
    return data


def read_checks(repo: Path) -> tuple[dict | None, str]:
    text = read_base_text(repo, ".verify/checks.json")
    if text is None:
        return None, "fail closed: base has no .verify/checks.json"
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None, "fail closed: base checks.json is not valid JSON"
    if not isinstance(data.get("checks"), list):
        return None, "fail closed: base checks.json has no checks list"
    return data, ""


def lock_patterns(checks: dict | None) -> list[str]:
    extra = []
    if checks and isinstance(checks.get("locked"), list):
        extra = [str(item) for item in checks["locked"]]
    return list(dict.fromkeys([*MINIMUM_LOCK, *extra]))


def test_patterns(checks: dict | None) -> list[str]:
    extra = []
    if checks and isinstance(checks.get("test_paths"), list):
        extra = [str(item) for item in checks["test_paths"]]
    return list(dict.fromkeys([*DEFAULT_TEST_PATHS, *extra]))


def porcelain(repo: Path) -> list[tuple[str, str]]:
    proc = git(repo, "status", "--porcelain", "--untracked-files=all")
    if proc.returncode != 0:
        return []
    entries: list[tuple[str, str]] = []
    for line in proc.stdout.splitlines():
        if len(line) < 4:
            continue
        status, path = line[:2], line[3:]
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        path = path.replace("\\", "/")
        if path in HASH_SKIP_FILES or "__pycache__" in path.split("/") or path.endswith(".pyc"):
            continue
        if status == "??":
            code = "A"
        elif "D" in status:
            code = "D"
        elif "A" in status and "M" not in status and "D" not in status:
            code = "A"
        else:
            code = "M"
        entries.append((code, path))
    return entries


def tree_hash(repo: Path) -> str:
    digest = hashlib.sha256()
    root = repo.resolve()
    files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(name for name in dirnames if name not in HASH_SKIP_DIRS)
        for name in sorted(filenames):
            files.append(Path(dirpath) / name)
    for path in files:
        rel = path.relative_to(root).as_posix()
        if rel in HASH_SKIP_FILES or path.is_symlink():
            continue
        digest.update(rel.encode())
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def state_file(repo: Path, session_id: str) -> Path:
    root = Path(os.environ.get("VERIFY_STATE_DIR", Path(tempfile.gettempdir()) / "verify-course"))
    key = hashlib.sha256(str(repo.resolve()).encode()).hexdigest()[:16]
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id)[:80] or "session"
    directory = root / key
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{safe}.json"


def log_path(repo: Path) -> Path:
    return state_file(repo, "x").parent / "gate.log"


def append_log(repo: Path, row: dict) -> None:
    path = log_path(repo)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")


def load_rounds(repo: Path, session_id: str) -> int:
    path = state_file(repo, session_id)
    if not path.exists():
        return 0
    try:
        return int(json.loads(path.read_text()).get("blocks", 0))
    except (json.JSONDecodeError, ValueError, OSError):
        return 0


def save_rounds(repo: Path, session_id: str, blocks: int) -> None:
    path = state_file(repo, session_id)
    path.write_text(json.dumps({"blocks": blocks}))


def clear_rounds(repo: Path, session_id: str) -> None:
    path = state_file(repo, session_id)
    if path.exists():
        path.unlink()


def added_source_lines(repo: Path) -> list[tuple[str, str]]:
    found: list[tuple[str, str]] = []
    proc = git(repo, "diff", "-U0", "HEAD")
    current = ""
    if proc.returncode == 0:
        for line in proc.stdout.splitlines():
            if line.startswith("+++ b/"):
                current = line[6:]
            elif line.startswith("+") and not line.startswith("+++") and current:
                found.append((current, line[1:]))
    for code, path in porcelain(repo):
        if code != "A":
            continue
        file_path = repo / path
        if not file_path.is_file():
            continue
        for line in file_path.read_text(encoding="utf-8", errors="replace").splitlines():
            found.append((path, line))
    return found


def tamper_problems(repo: Path) -> list[str]:
    problems: list[str] = []
    grouped: dict[str, list[str]] = {}
    for path, line in added_source_lines(repo):
        if Path(path).suffix not in SOURCE_SUFFIXES:
            continue
        grouped.setdefault(path, []).append(line)
        lowered = line.lower()
        if any(
            token in line
            for token in ("#[ignore]", "pytest.mark.skip", "pytest.skip", "unittest.skip")
        ):
            problems.append(f"silent skip added in {path}")
        if re.search(r"test_name\s*==", line) or re.search(r"==\s*['\"]test_", line):
            problems.append(f"test-name special case in {path}")
        if "PYTEST_CURRENT_TEST" in line:
            problems.append(f"test-name special case in {path}")
        if "call_count" in lowered:
            problems.append(f"call-count state in {path}")
    for path, lines in grouped.items():
        blob = "\n".join(lines)
        if ("fn eq(" in blob or "__eq__" in blob) and ("return true" in blob or "return True" in blob):
            problems.append(f"equality override in {path}")
    return problems


def test_policy_problems(repo: Path, patterns: list[str], allow_existing_edits: bool) -> list[str]:
    if allow_existing_edits:
        return []
    problems = []
    for code, path in porcelain(repo):
        if not any(glob_match(pattern, path) for pattern in patterns):
            continue
        if code == "D":
            problems.append(f"existing test deleted: {path}")
        elif code == "M":
            problems.append(f"existing test modified: {path}")
    return problems


def scope_problems(repo: Path, changed: list[str]) -> list[str]:
    pointer = read_base_text(repo, ".verify/active-brief")
    if pointer is None or not pointer.strip():
        return []
    rel = pointer.strip().splitlines()[0].strip()
    text = read_base_text(repo, rel)
    if text is None:
        return [f"fail closed: active brief {rel} is not on the base ref"]
    allowed = allowed_globs(text)
    if not allowed:
        return ["fail closed: active brief lists no allowed files"]
    problems = []
    for path in changed:
        if any(glob_match(pattern, path) for pattern in allowed):
            continue
        problems.append(f"scope creep: {path} is outside the active brief")
    return problems


def triggered_checks(checks: dict, changed: list[str]) -> list[dict]:
    chosen = []
    for check in checks.get("checks", []):
        patterns = check.get("when") or []
        if any(glob_match(pattern, path) for path in changed for pattern in patterns):
            chosen.append(check)
    return chosen


def run_command(cmd: str, repo: Path) -> dict:
    timeout = float(os.environ.get("VERIFY_COMMAND_TIMEOUT", "180"))
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        proc = subprocess.run(
            cmd,
            cwd=repo,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        exit_code = proc.returncode
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
    except subprocess.TimeoutExpired as exc:
        exit_code = 124
        stdout = exc.stdout or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        stderr = exc.stderr or ""
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
    return {
        "cmd": cmd,
        "exit_code": exit_code,
        "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
        "stderr_sha256": hashlib.sha256(stderr.encode()).hexdigest(),
    }


def run_verify(repo: Path, allow_test_change: bool = False) -> Report:
    before = tree_hash(repo)
    changed_entries = porcelain(repo)
    changed = [path for _, path in changed_entries]
    checks, error = read_checks(repo)
    problems: list[str] = []
    if error:
        problems.append(error)
    patterns = lock_patterns(checks)
    for path in changed:
        if is_locked(path, patterns):
            problems.append(f"locked path changed: {path}")
    problems.extend(test_policy_problems(repo, test_patterns(checks), allow_test_change))
    problems.extend(tamper_problems(repo))
    problems.extend(scope_problems(repo, changed))
    commands: list[dict] = []
    triggered: list[str] = []
    if checks and not any(item.startswith("locked path") for item in problems):
        for check in triggered_checks(checks, changed):
            check_id = str(check.get("id", "unnamed"))
            triggered.append(check_id)
            command = str(check.get("check", ""))
            if not command.strip():
                problems.append(f"check {check_id} has an empty command")
                continue
            result = run_command(command, repo)
            result["id"] = check_id
            commands.append(result)
            if result["exit_code"] != 0:
                problems.append(f"check {check_id} exited {result['exit_code']}")
    after = tree_hash(repo)
    if before != after:
        problems.append("a check changed the tree it was judging")
    verdict = "PASS" if not problems else "FAIL"
    report = Report(verdict, problems, before, commands, triggered, changed)
    write_evidence(repo, report)
    return report


def write_evidence(repo: Path, report: Report) -> None:
    directory = repo / ".verify"
    directory.mkdir(parents=True, exist_ok=True)
    body = report.to_evidence()
    (directory / "evidence.json").write_text(json.dumps(body, indent=2) + "\n")
    lines = [
        "# Evidence",
        "",
        f"VERDICT: {report.verdict}",
        f"TREE: {report.tree_hash}",
        "PRODUCED_BY: verify_runner",
        "",
        "This file is generated. Editing the verdict does not make it true.",
        "CI runs the checks again.",
        "",
        "## Commands",
    ]
    if report.commands:
        for command in report.commands:
            lines.append(f"- {command['id']} exit {command['exit_code']}")
    else:
        lines.append("- (none triggered)")
    if report.problems:
        lines.extend(["", "## Problems"])
        lines.extend(f"- {problem}" for problem in report.problems)
    lines.extend(
        [
            "",
            "## Narrative",
            "E2E:",
            "NOT CHECKED:",
            "",
        ]
    )
    (directory / "evidence.md").write_text("\n".join(lines))


def audit_evidence_file(repo: Path) -> list[str]:
    path = repo / ".verify" / "evidence.json"
    if not path.exists():
        return ["evidence.json is missing"]
    try:
        body = json.loads(path.read_text())
    except json.JSONDecodeError:
        return ["evidence.json is not valid JSON"]
    problems = []
    if body.get("produced_by") != "verify_runner":
        problems.append("evidence was not produced by verify_runner")
    if body.get("integrity") != integrity(body):
        problems.append("evidence integrity hash does not match its contents")
    command_failures = [item for item in body.get("commands", []) if item.get("exit_code") != 0]
    claimed = body.get("verdict")
    if claimed == "PASS" and (command_failures or body.get("problems")):
        problems.append("verdict PASS disagrees with recorded failures")
    if body.get("tree_hash") != tree_hash(repo):
        problems.append("evidence tree hash does not match the worktree")
    return problems


def _finish(repo: Path, decision: Decision, event: dict) -> Decision:
    append_log(
        repo,
        {
            "code": decision.code,
            "allow": decision.allow,
            "message": decision.message,
            "session_id": event.get("session_id", ""),
            "hook_event_name": event.get("hook_event_name", ""),
            "stop_hook_active": bool(event.get("stop_hook_active", False)),
        },
    )
    return decision


def decide_stop(event: dict, repo: Path) -> Decision:
    if event.get("_invalid"):
        return _finish(repo, Decision(False, "BLOCK", "fail closed: hook input was not valid JSON"), event)
    name = event.get("hook_event_name")
    if name not in ("Stop", "SubagentStop"):
        return _finish(repo, Decision(True, "IGNORE", "not a stop event"), event)
    gate = read_gate(repo)
    mode = gate["mode"]
    if mode == "off":
        return _finish(repo, Decision(True, "OFF", "base gate mode is off; nothing was enforced"), event)
    report = run_verify(repo, allow_test_change=False)
    session = str(event.get("session_id") or "unknown")
    active = bool(event.get("stop_hook_active", False))
    if report.verdict == "PASS":
        clear_rounds(repo, session)
        message = f"verify passed; stop_hook_active={str(active).lower()}"
        code = "OBSERVE" if mode == "observe" else "PASS"
        return _finish(repo, Decision(True, code, message), event)
    rounds = load_rounds(repo, session) + 1
    save_rounds(repo, session, rounds)
    cap = int(gate.get("platform_continuation_cap", 8))
    limit = int(gate.get("max_stop_rounds", 2))
    detail = "; ".join(report.problems) or "verify failed"
    message = f"round {rounds}; stop_hook_active={str(active).lower()}; {detail}"
    if rounds > limit or rounds > cap:
        _write_needs_human(repo, session, rounds, detail)
        code = "NEEDS_HUMAN" if rounds > limit else "PLATFORM_CAP"
        if rounds > limit and rounds > cap:
            code = "NEEDS_HUMAN"
        if mode == "observe":
            return _finish(repo, Decision(True, "OBSERVE", f"would escalate ({code}): {message}"), event)
        return _finish(repo, Decision(True, code, message), event)
    if mode == "observe":
        return _finish(repo, Decision(True, "OBSERVE", f"would block: {message}"), event)
    return _finish(repo, Decision(False, "BLOCK", message), event)


def _write_needs_human(repo: Path, session: str, rounds: int, detail: str) -> None:
    directory = repo / ".verify"
    directory.mkdir(parents=True, exist_ok=True)
    text = (
        "# NEEDS-HUMAN\n\n"
        f"session: {session}\n"
        f"rounds: {rounds}\n"
        f"detail: {detail}\n\n"
        "The gate stopped blocking so a person can look. This is not a pass.\n"
    )
    (directory / "NEEDS-HUMAN.md").write_text(text)


def split_commands(command: str) -> list[list[str]]:
    commands: list[list[str]] = []
    current: list[str] = []
    token: list[str] = []
    quote: str | None = None
    index = 0
    while index < len(command):
        char = command[index]
        if quote:
            if char == quote:
                quote = None
            else:
                token.append(char)
            index += 1
            continue
        if char in ("'", '"'):
            quote = char
            index += 1
            continue
        if char.isspace():
            if token:
                current.append("".join(token))
                token = []
            index += 1
            continue
        if command.startswith("&&", index) or command.startswith("||", index):
            if token:
                current.append("".join(token))
                token = []
            if current:
                commands.append(current)
                current = []
            index += 2
            continue
        if char in (";", "|", "\n"):
            if token:
                current.append("".join(token))
                token = []
            if current:
                commands.append(current)
                current = []
            index += 1
            continue
        token.append(char)
        index += 1
    if token:
        current.append("".join(token))
    if current:
        commands.append(current)
    return commands


def _is_commit(argv: list[str]) -> tuple[bool, str, dict[str, str]]:
    if not argv:
        return False, "", {}
    if Path(argv[0]).name != "git":
        return False, "", {}
    index = 1
    args = argv
    while index < len(args):
        arg = args[index]
        if arg in ("-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"):
            index += 2
            continue
        if arg.startswith("-c") and arg != "-C":
            index += 1
            continue
        if arg.startswith(("--git-dir=", "--work-tree=", "--namespace=", "--exec-path=")):
            index += 1
            continue
        if arg in ("--no-pager", "--paginate", "--bare", "--literal-pathspecs", "-P"):
            index += 1
            continue
        break
    if index >= len(args) or args[index] != "commit":
        return False, "", {}
    index += 1
    messages: list[str] = []
    trailers: dict[str, str] = {}
    while index < len(args):
        arg = args[index]
        if arg in ("-m", "--message") and index + 1 < len(args):
            messages.append(args[index + 1])
            index += 2
            continue
        if arg.startswith("--message="):
            messages.append(arg.split("=", 1)[1])
            index += 1
            continue
        if arg == "--trailer" and index + 1 < len(args):
            key, _, value = args[index + 1].partition(":")
            trailers[key.strip().lower()] = value.strip()
            index += 2
            continue
        if arg.startswith("--trailer="):
            key, _, value = arg.split("=", 1)[1].partition(":")
            trailers[key.strip().lower()] = value.strip()
            index += 1
            continue
        if arg in ("-F", "--file", "--author", "--date") and index + 1 < len(args):
            index += 2
            continue
        index += 1
    message = "\n\n".join(messages)
    trailers.update(parse_trailers(message))
    return True, message, trailers


def parse_trailers(message: str) -> dict[str, str]:
    lines = message.replace("\r\n", "\n").split("\n")
    last_blank = -1
    for index, line in enumerate(lines):
        if line.strip() == "":
            last_blank = index
    block = lines[last_blank + 1 :] if last_blank >= 0 else lines
    matched = []
    for line in block:
        found = re.match(r"^([A-Za-z0-9-]+):\s*(.*)$", line)
        if not found:
            return {}
        matched.append(found)
    return {item.group(1).lower(): item.group(2).strip() for item in matched}


def _command_is_opaque(command: str) -> bool:
    return "$(" in command or "`" in command


def decide_commit(event: dict, repo: Path) -> Decision:
    if event.get("_invalid"):
        return _finish(repo, Decision(False, "BLOCK", "fail closed: hook input was not valid JSON"), event)
    if event.get("hook_event_name") != "PreToolUse" or event.get("tool_name") != "Bash":
        return _finish(repo, Decision(True, "IGNORE", "not a Bash PreToolUse event"), event)
    tool_input = event.get("tool_input") or {}
    command = tool_input.get("command", "")
    if not isinstance(command, str) or not command.strip():
        return _finish(repo, Decision(False, "BLOCK", "fail closed: missing command string"), event)
    if _command_is_opaque(command) and re.search(r"\bgit\b", command) and re.search(r"\bcommit\b", command):
        return _finish(
            repo,
            Decision(False, "BLOCK", "fail closed: a git commit is hidden by command substitution"),
            event,
        )
    commits = []
    for argv in split_commands(command):
        is_commit, message, trailers = _is_commit(argv)
        if is_commit:
            commits.append((message, trailers))
    if not commits:
        return _finish(repo, Decision(True, "ALLOW", "not a git commit"), event)
    trailers: dict[str, str] = {}
    for _message, extra in commits:
        trailers.update(extra)
    lowered = command.lower()
    substring = "verified-by: none" in lowered or "verified-by:none" in lowered
    exempt = trailers.get("verified-by", "").lower() == "none"
    if substring and not exempt:
        return _finish(
            repo,
            Decision(
                False,
                "BLOCK",
                "Verified-by: none only counts as a parsed trailer, not as a substring",
            ),
            event,
        )
    if exempt and not strong_reason(trailers.get("exemption-reason", "")):
        return _finish(
            repo,
            Decision(False, "BLOCK", "Verified-by: none requires a substantive Exemption-reason trailer"),
            event,
        )
    gate = read_gate(repo)
    checks, _error = read_checks(repo)
    patterns = lock_patterns(checks)
    dirty_locks = [path for _code, path in porcelain(repo) if is_locked(path, patterns)]
    if dirty_locks:
        return _finish(
            repo,
            Decision(False, "BLOCK", "locked path changed: " + ", ".join(dirty_locks)),
            event,
        )
    tamper = tamper_problems(repo)
    if tamper:
        return _finish(repo, Decision(False, "BLOCK", "; ".join(tamper)), event)
    scope = scope_problems(repo, [path for _code, path in porcelain(repo)])
    if scope:
        return _finish(repo, Decision(False, "BLOCK", "; ".join(scope)), event)
    allow_tests = strong_reason(trailers.get("test-change-approved", ""))
    test_problems = test_policy_problems(repo, test_patterns(checks), allow_tests)
    if test_problems:
        return _finish(repo, Decision(False, "BLOCK", "; ".join(test_problems)), event)
    if gate["mode"] == "off":
        return _finish(repo, Decision(True, "OFF", "base gate mode is off"), event)
    if exempt:
        code = "OBSERVE" if gate["mode"] == "observe" else "EXEMPT"
        return _finish(
            repo,
            Decision(True, code, "exemption recorded; CI still re-runs the checks and can reject the push"),
            event,
        )
    report = run_verify(repo, allow_test_change=allow_tests)
    if report.verdict != "PASS":
        message = "; ".join(report.problems) or "verify failed"
        if gate["mode"] == "observe":
            return _finish(repo, Decision(True, "OBSERVE", f"would block: {message}"), event)
        return _finish(repo, Decision(False, "BLOCK", message), event)
    code = "OBSERVE" if gate["mode"] == "observe" else "PASS"
    return _finish(repo, Decision(True, code, "verify passed"), event)


def render_stop(decision: Decision) -> str:
    if decision.allow:
        return ""
    return json.dumps({"decision": "block", "reason": decision.message}) + "\n"


def render_commit(decision: Decision) -> str:
    if decision.allow:
        return ""
    body = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": decision.message,
        }
    }
    return json.dumps(body) + "\n"


def structural_problems(repo: Path) -> tuple[list[str], list[str]]:
    """Problems that do not require running check commands, plus triggered ids."""
    changed = [path for _code, path in porcelain(repo)]
    checks, error = read_checks(repo)
    problems: list[str] = []
    if error:
        problems.append(error)
    for path in changed:
        if is_locked(path, lock_patterns(checks)):
            problems.append(f"locked path changed: {path}")
    problems.extend(test_policy_problems(repo, test_patterns(checks), False))
    problems.extend(tamper_problems(repo))
    problems.extend(scope_problems(repo, changed))
    triggered = [str(check.get("id", "unnamed")) for check in triggered_checks(checks or {}, changed)]
    return problems, triggered
