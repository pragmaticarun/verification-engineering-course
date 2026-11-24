#!/usr/bin/env bash
# cargo-mutants 26.0.0 on clamp.rs only. Not a crate-wide mutation score.
# Two mutants are equivalent: replacing > with >= and < with <= still returns
# the same rail when the sample is exactly 1 or -1. Jobs stay at 1 because a
# parallel run against one target directory has reported false misses.
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"
# Nightly Miri and the fuzzer use other directories under target/.
export CARGO_TARGET_DIR="$root/target/mutants"
out="$(mktemp)"
set +e
cargo mutants --version
cargo mutants \
  --manifest-path pcmkit/Cargo.toml \
  --file crates/pcmkit/src/clamp.rs \
  --timeout 60 \
  --jobs 1 \
  --no-config \
  | tee "$out"
code=$?
set -e
python3 - "$out" "$code" <<'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
code = int(sys.argv[2])
missed = []
for line in text.splitlines():
    if not line.startswith("MISSED"):
        continue
    missed.append(re.sub(r" in \d+s build \+ \d+s test$", "", line).rstrip())
expected = [
    "MISSED   crates/pcmkit/src/clamp.rs:19:15: replace > with >= in clamp_unit",
    "MISSED   crates/pcmkit/src/clamp.rs:21:22: replace < with <= in clamp_unit",
]
if code != 2:
    raise SystemExit(f"cargo-mutants exit {code}, expected 2 for the two equivalent mutants")
if missed != expected:
    raise SystemExit("unexpected misses:\n" + "\n".join(missed))
if "9 caught" not in text:
    raise SystemExit("expected 9 caught mutants")
print("mutants smoke ok: 9 caught, 2 equivalent misses")
PY
rm -f "$out"
