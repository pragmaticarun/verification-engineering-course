"""Two quantizers. One rounds. One truncates."""

from __future__ import annotations

import math


def quantize_i16(sample: float) -> int:
    x = max(-1.0, min(1.0, sample)) * 32768.0
    if x >= 0.0:
        rounded = math.floor(x + 0.5)
    else:
        rounded = math.ceil(x - 0.5)
    return max(-32768, min(32767, int(rounded)))


def quantize_toward_zero(sample: float) -> int:
    x = max(-1.0, min(1.0, sample)) * 32768.0
    return max(-32768, min(32767, int(x)))
