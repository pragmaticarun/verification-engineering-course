#!/usr/bin/env bash
# Kani 0.68.0 on one proof. The first `cargo kani` downloads the 0.68 bundle
# and installs nightly-2026-08-21, which is the toolchain that bundle pins.
# The course's rust-toolchain.toml stays on 1.83.0. This package is excluded
# from the workspace.
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root/pcmkit/kani"
export CARGO_TARGET_DIR="$root/target/kani"
cargo kani --version
cargo kani --harness clamp_unit_holds_an_i8_grid
echo "kani smoke ok: clamp_unit_holds_an_i8_grid"
