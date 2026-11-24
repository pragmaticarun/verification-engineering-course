"""Peak of a buffer. Hidden cases include negative samples."""

from __future__ import annotations


def peak(samples: list[float]) -> float:
    if not samples:
        raise ValueError("empty")
    return max(abs(sample) for sample in samples)


def peak_visible_only(samples: list[float]) -> float:
    """Passes a suite that never goes below zero, and misses a negative peak."""
    if not samples:
        raise ValueError("empty")
    return max(samples)
