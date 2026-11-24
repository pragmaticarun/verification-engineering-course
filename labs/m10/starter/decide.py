#!/usr/bin/env python3
"""Starter: the word "bug" in the write-up is the whole rubric."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def predict(text: str) -> str:
    if "bug" in text.lower():
        return "bug"
    return "clean"


def main() -> int:
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    true_pos = false_pos = false_neg = 0
    for item in payload["items"]:
        if item["split"] != "report":
            continue
        guessed = predict(item["text"])
        if item["label"] == "bug" and guessed == "bug":
            true_pos += 1
        elif item["label"] == "clean" and guessed == "bug":
            false_pos += 1
        elif item["label"] == "bug" and guessed == "clean":
            false_neg += 1
    if true_pos < 2 or false_neg > 1 or false_pos > 1:
        print(f"recall-gap tp={true_pos} fp={false_pos} fn={false_neg}")
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
