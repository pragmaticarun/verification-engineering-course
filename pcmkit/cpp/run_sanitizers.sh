#!/usr/bin/env bash
# UBSan and ASan on the C++ consumer. The Rust static library is built with
# the ordinary stable toolchain, so the sanitizers see the C++ side of the
# ABI call, not every instruction inside the Rust library. That limit is
# stated in module 7. A full Rust ASan build needs a sanitizer-enabled rustc
# and is not this script.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
PCM="$(cd "$HERE/.." && pwd)"
COURSE="$(cd "$PCM/.." && pwd)"
export CARGO_TARGET_DIR="${CARGO_TARGET_DIR:-$COURSE/target}"
export CXX="${CXX:-g++}"

cargo build --manifest-path "$PCM/Cargo.toml" -p pcmkit-ffi --offline
cmake -S "$HERE" -B "$HERE/build-san" \
  -DPCM_LIB="$CARGO_TARGET_DIR/debug/libpcmkit_ffi.a" \
  -DPCM_SANITIZERS=ON
cmake --build "$HERE/build-san"
"$HERE/build-san/consumer"
