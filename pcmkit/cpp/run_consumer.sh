#!/usr/bin/env bash
# Build the C ABI and the C++ consumer, then run the consumer.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PCM="$(cd "$HERE/.." && pwd)"
COURSE="$(cd "$PCM/.." && pwd)"
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$COURSE/target}"
# clang++ is sometimes installed as /usr/bin/c++ without a usable libstdc++.
export CXX="${CXX:-g++}"

cargo build --manifest-path "$PCM/Cargo.toml" -p pcmkit-ffi --offline
cmake -S "$HERE" -B "$HERE/build" -DPCM_LIB="$CARGO_TARGET_DIR/debug/libpcmkit_ffi.a"
cmake --build "$HERE/build"
"$HERE/build/consumer"
