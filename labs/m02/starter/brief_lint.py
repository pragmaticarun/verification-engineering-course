#!/usr/bin/env python3
"""Accept any file that starts with a brief heading.

The starter does not look for an acceptance command, non-goals, or an
allowed-file list. A vague brief passes.
"""

from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    text = Path(sys.argv[1]).read_text()
    if text.lstrip().startswith("# Brief:"):
        print("ok")
        return 0
    print("not a brief")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
