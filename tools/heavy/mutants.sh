#!/usr/bin/env bash
# cargo-mutants 26.0.0 on clamp.rs only. Not a crate-wide mutation score.
# Two mutants are equivalent: replacing > with >= and < with <= still returns
# the same rail when the sample is exactly 1 or -1. Jobs stay at 1 because a
# parallel run against one target directory has reported false misses.
# Colors are off. The allowlist is mutants.out/missed.txt, compared on
# file, line, and mutation text, not on the painted log line.
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root"
# Nightly Miri and the fuzzer use other directories under target/.
export CARGO_TARGET_DIR="$root/target/mutants"
export CARGO_TERM_COLOR=never
out_dir="$root/target/mutants-report"
rm -rf "$out_dir"
set +e
cargo mutants --version
cargo mutants \
  --manifest-path pcmkit/Cargo.toml \
  --file crates/pcmkit/src/clamp.rs \
  --timeout 60 \
  --jobs 1 \
  --no-config \
  --colors never \
  -o "$out_dir"
code=$?
set -e
python3 "$root/tools/heavy/mutant_report.py" \
  "$out_dir/mutants.out/missed.txt" \
  "$out_dir/mutants.out/caught.txt" \
  "$code"
