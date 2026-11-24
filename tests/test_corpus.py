"""The recorded-event corpus is the harness self-test."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from mockagent.replay import run_corpus  # noqa: E402


class Corpus(unittest.TestCase):
    def test_every_recorded_scenario(self) -> None:
        failed = [item for item in run_corpus() if not item.ok]
        self.assertEqual([(item.name, item.detail) for item in failed], [])


if __name__ == "__main__":
    unittest.main()
