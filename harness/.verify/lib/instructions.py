"""Check that Claude, Codex, and Cursor are told the same definition of done."""

from __future__ import annotations

import json
from pathlib import Path

DONE_SENTENCE = "Done is a claim: a command exited 0 on this tree."
CODEX_BYTE_LIMIT = 32 * 1024

INSTRUCTION_FILES = (
    "CLAUDE.md",
    "AGENTS.md",
    ".cursor/rules/verification.mdc",
    "REVIEW.md",
)


def combined_agents_bytes(root: Path, cwd: Path | None = None) -> int:
    """Bytes Codex would concatenate walking from `root` down to `cwd`."""
    root = root.resolve()
    cwd = (cwd or root).resolve()
    total = 0
    current = cwd
    seen: list[Path] = []
    while True:
        for name in ("AGENTS.override.md", "AGENTS.md"):
            candidate = current / name
            if candidate.is_file() and candidate.stat().st_size > 0:
                seen.append(candidate)
                break
        if current == root:
            break
        if root not in current.parents and current != root:
            break
        parent = current.parent
        if parent == current:
            break
        current = parent
    for path in reversed(seen):
        total += path.stat().st_size + 1
    return total


def audit(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in INSTRUCTION_FILES:
        path = root / rel
        if not path.is_file():
            errors.append(f"missing {rel}")
            continue
        if DONE_SENTENCE not in path.read_text(encoding="utf-8"):
            errors.append(f"{rel} does not state the shared done sentence")
    agents = root / "AGENTS.md"
    if agents.is_file() and agents.stat().st_size > CODEX_BYTE_LIMIT:
        errors.append("AGENTS.md exceeds Codex's default 32 KiB project_doc_max_bytes")
    if combined_agents_bytes(root) > CODEX_BYTE_LIMIT:
        errors.append("concatenated AGENTS.md files exceed 32 KiB")
    settings_path = root / ".claude" / "settings.json"
    if not settings_path.is_file():
        errors.append("missing .claude/settings.json")
        return errors
    try:
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        errors.append("settings.json is not valid JSON")
        return errors
    deny = settings.get("permissions", {}).get("deny", [])
    if not isinstance(deny, list):
        errors.append("permissions.deny must be a list")
        deny = []
    blob = "\n".join(str(item) for item in deny)
    if ".verify" not in blob or ".claude" not in blob:
        errors.append("permissions.deny does not cover .verify and .claude")
    hooks = settings.get("hooks", {})
    if "Stop" not in hooks or "PreToolUse" not in hooks:
        errors.append("settings.json does not register Stop and PreToolUse")
    return errors
