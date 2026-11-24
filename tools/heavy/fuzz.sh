#!/usr/bin/env bash
# cargo-fuzz 0.13.2 on the WAV parser for 15 seconds.
# The binary is built with nightly-2026-11-23 because 0.13.2 depends on
# crates that need Cargo edition 2024. Rust 1.83.0, the course pin, cannot
# compile those crates. The package is excluded from the workspace so the
# light job never links libFuzzer.
set -euo pipefail
root="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$root/pcmkit"
# Keep nightly fuzz objects out of the stable target directory.
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$root/target}/fuzz-nightly"
# This image's /usr/bin/c++ is clang, and rust-lld does not search GCC's
# libstdc++ by default. GitHub's ubuntu-24.04 image usually does. Adding the
# path is a no-op when the files are already on the default search path.
gcc_ver="$(g++ -dumpversion | cut -d. -f1)"
export CPLUS_INCLUDE_PATH="/usr/include/c++/${gcc_ver}:/usr/include/x86_64-linux-gnu/c++/${gcc_ver}${CPLUS_INCLUDE_PATH:+:$CPLUS_INCLUDE_PATH}"
gcc_lib="$(g++ -print-file-name=libstdc++.so)"
export LIBRARY_PATH="$(dirname "$gcc_lib")${LIBRARY_PATH:+:$LIBRARY_PATH}"
cargo +nightly-2026-11-23 fuzz --version
cargo +nightly-2026-11-23 fuzz run wav_parser -- -max_total_time=15 -timeout=10
echo "fuzz smoke ok: wav_parser ran for 15 seconds"
