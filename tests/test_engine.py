"""Small pure checks that do not need a git repository."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "harness" / ".verify"))

from lib.engine import (  # noqa: E402
    _is_commit,
    command_notes,
    glob_match,
    parse_trailers,
    split_commands,
    strong_reason,
)


class Engine(unittest.TestCase):
    def test_globs(self) -> None:
        self.assertTrue(glob_match("pcmkit/**/*.rs", "pcmkit/crates/pcmkit/src/lib.rs"))
        self.assertFalse(glob_match("pcmkit/**/*.rs", "labs/m01/starter/review.py"))
        self.assertTrue(glob_match("**/*_test.py", "sample_test.py"))

    def test_commit_parser_ignores_commit_tree_and_reads_trailers(self) -> None:
        commands = split_commands('git -c user.email=a@b.c commit -m "ship" -m "Verified-by: none"')
        self.assertEqual(len(commands), 1)
        is_commit, _message, trailers = _is_commit(commands[0])
        self.assertTrue(is_commit)
        self.assertEqual(trailers.get("verified-by"), "none")
        other = split_commands("git commit-tree HEAD -m ship")
        self.assertFalse(_is_commit(other[0])[0])

    def test_strong_reason_rejects_placeholders(self) -> None:
        self.assertFalse(strong_reason("later"))
        self.assertFalse(strong_reason("too short"))
        self.assertTrue(strong_reason("Listened on headphones; the click is in the source."))

    def test_command_notes_keep_e2e_lines_and_ignore_prose(self) -> None:
        notes = command_notes("building\nE2E: pcmx matched\nNOT CHECKED: listening\nVERDICT: PASS\n")
        self.assertEqual(notes, ["E2E: pcmx matched", "NOT CHECKED: listening"])

    def test_trailers_do_not_match_a_mention_in_prose(self) -> None:
        message = "Fix the clamp\n\nDo not write Verified-by: none in prose."
        self.assertEqual(parse_trailers(message), {})


if __name__ == "__main__":
    unittest.main()
