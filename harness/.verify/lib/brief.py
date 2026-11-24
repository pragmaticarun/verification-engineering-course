"""Parse a task brief. The brief is the definition of done for one change."""

from __future__ import annotations

import re
from pathlib import Path

REQUIRED = ("Goal", "Acceptance", "Non-goals", "Allowed-files")


def sections(text: str) -> dict[str, str]:
    parts = re.split(r"(?m)^## ", text)
    found: dict[str, str] = {}
    for part in parts[1:]:
        lines = part.splitlines()
        title = lines[0].strip()
        found[title] = "\n".join(lines[1:]).strip()
    return found


def bullet_items(body: str) -> list[str]:
    items = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            items.append(stripped[2:].strip())
    return items


def acceptance_command(body: str) -> str:
    for line in body.splitlines():
        if line.strip().lower().startswith("command:"):
            return line.split(":", 1)[1].strip()
    return ""


def lint_brief(text: str, root: Path | None = None) -> list[str]:
    """Return human-readable problems. An empty list means the brief is usable."""
    errors: list[str] = []
    first = text.strip().splitlines()[0] if text.strip() else ""
    if not first.startswith("# Brief:") or not first.split(":", 1)[1].strip():
        errors.append("first line must be '# Brief: <title>'")
    found = sections(text)
    for name in REQUIRED:
        if name not in found or not found[name].strip():
            errors.append(f"missing or empty section '## {name}'")
    if "Non-goals" in found and not bullet_items(found["Non-goals"]):
        errors.append("Non-goals needs at least one bullet")
    allowed = bullet_items(found.get("Allowed-files", ""))
    if "Allowed-files" in found and not allowed:
        errors.append("Allowed-files needs at least one path")
    acceptance = found.get("Acceptance", "")
    command = acceptance_command(acceptance)
    if "Acceptance" in found and not command:
        errors.append("Acceptance needs a 'command:' line")
    if "Acceptance" in found and not re.search(r"(?im)^expect_exit:\s*\d+\s*$", acceptance):
        errors.append("Acceptance needs an 'expect_exit:' line")
    if root is not None and command:
        for token in command.split():
            if token.startswith("-"):
                continue
            if "/" in token or token.endswith((".py", ".sh")):
                if not (root / token).exists():
                    errors.append(f"acceptance path does not exist: {token}")
    return errors


def allowed_globs(text: str) -> list[str]:
    return bullet_items(sections(text).get("Allowed-files", ""))
