"""Every fenced example in the course is a file CI runs, a diagram, or plain text."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

SNIPPET = re.compile(r'--8<--\s+"([^"]+)"')
FENCE = re.compile(r"^(`{3,})([^\n`]*)\n(.*?)^\1", re.M | re.S)
PLAIN = {"", "text", "mermaid"}
# These trees are executed by `make check` (cargo, the oracle, the consumer,
# unittest, or the acceptance command). A snippet from anywhere else has to be
# named by a test, a tool, or the Makefile.
EXERCISED_PREFIXES = (
    "pcmkit/",
    ".github/workflows/",
    "labs/",
    "harness/",
    "briefs/",
    "scenarios/",
    "tools/",
    "tests/",
)


class DocsExamples(unittest.TestCase):
    def test_nav_pages_exist(self) -> None:
        config = (ROOT / "mkdocs.yml").read_text(encoding="utf-8")
        for match in re.finditer(r":\s+(\S+\.md)\s*$", config, re.M):
            rel = match.group(1)
            self.assertTrue((DOCS / rel).is_file(), rel)

    def test_fences_are_snippets_or_diagrams(self) -> None:
        for path in sorted(DOCS.rglob("*.md")):
            for fence in FENCE.finditer(path.read_text(encoding="utf-8")):
                info = fence.group(2).strip()
                lang = info.split()[0] if info else ""
                if lang in PLAIN:
                    continue
                self.assertIn(
                    "--8<--",
                    fence.group(3),
                    f"{path.relative_to(ROOT)} has a `{lang}` fence that is not a snippet",
                )

    def test_snippets_point_at_files_ci_runs(self) -> None:
        mentions = []
        for folder in ("tests", "tools", "labs", "harness"):
            for path in (ROOT / folder).rglob("*"):
                if path.suffix in {".py", ".sh", ".json", ".md", ".yml", ".yaml"}:
                    mentions.append(path.read_text(encoding="utf-8", errors="ignore"))
        mentions.append((ROOT / "Makefile").read_text(encoding="utf-8"))
        blob = "\n".join(mentions)
        for path in sorted(DOCS.rglob("*.md")):
            for match in SNIPPET.finditer(path.read_text(encoding="utf-8")):
                rel = match.group(1).split(":", 1)[0]
                target = ROOT / rel
                self.assertTrue(target.is_file(), rel)
                if rel.startswith(EXERCISED_PREFIXES):
                    continue
                name = Path(rel).name
                self.assertTrue(name in blob or rel in blob, rel)


if __name__ == "__main__":
    unittest.main()
