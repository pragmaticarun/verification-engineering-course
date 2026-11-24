#!/usr/bin/env bash
# clang-tidy on the consumer. The version is whatever `clang-tidy` is on
# PATH. CI installs the Ubuntu clang-tidy package and records it in the log.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
INCLUDE="$(cd "$HERE/.." && pwd)/include"
clang-tidy --version | head -n 1
# Narrow checks. The directory .clang-tidy is the wider set for a later
# module; this script is the one CI runs, and --config replaces that file.
clang-tidy "$HERE/tests/consumer.cpp" \
  --config="{Checks: '-*,bugprone-*,clang-analyzer-*', WarningsAsErrors: '*'}" \
  -- \
  -std=c++17 \
  -I "$INCLUDE" \
  -I /usr/include/c++/13 \
  -I /usr/include/x86_64-linux-gnu/c++/13
