#!/usr/bin/env python3
"""Score one rubric reviewer on mocked write-ups.

Precision and recall are computed on the report split only. The tune split is
how you would edit the rubric. It is not the number you publish.

The model text is a fixture. Nothing here calls a model.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def predict(text: str) -> str:
    """Bug only when the write-up quotes a failing exit. Otherwise clean."""
    if "exit 1" in text:
        return "bug"
    return "clean"


def score(items: list[dict], split: str) -> tuple[int, int, int, int]:
    true_pos = false_pos = false_neg = true_neg = 0
    for item in items:
        if item["split"] != split:
            continue
        guessed = predict(item["text"])
        if item["label"] == "bug" and guessed == "bug":
            true_pos += 1
        elif item["label"] == "clean" and guessed == "bug":
            false_pos += 1
        elif item["label"] == "bug" and guessed == "clean":
            false_neg += 1
        else:
            true_neg += 1
    return true_pos, false_pos, false_neg, true_neg


def fraction(num: int, den: int) -> str:
    return f"{num}/{den}"


def covers(proposal: dict) -> bool:
    if proposal["bug"] == "sign":
        return any(sample < 0 for sample in proposal["inputs"])
    return True


def main() -> int:
    reviews = json.loads((HERE / "reviews.json").read_text(encoding="utf-8"))
    proposals = json.loads((HERE / "proposals.json").read_text(encoding="utf-8"))
    true_pos, false_pos, false_neg, true_neg = score(reviews["items"], "report")
    tune = sum(1 for item in reviews["items"] if item["split"] == "tune")
    rejected = [item["id"] for item in proposals if not covers(item)]
    if true_pos + false_pos == 0 or true_pos + false_neg == 0:
        print("empty report split", file=sys.stderr)
        return 1
    print("split report")
    print(f"precision {fraction(true_pos, true_pos + false_pos)}")
    print(f"recall {fraction(true_pos, true_pos + false_neg)}")
    print(f"true_neg {true_neg}")
    print(f"tune_excluded {tune}")
    print(f"adversary_rejected {len(rejected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
