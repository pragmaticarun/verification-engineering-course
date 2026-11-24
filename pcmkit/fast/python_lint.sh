#!/usr/bin/env bash
# Ruff and mypy on the Python that the fast tier and the end-to-end proof own.
# Versions are pinned in requirements-checks.txt. CI installs that file.
set -euo pipefail
cd "$(dirname "$0")/../.."
python3 -m ruff check pcmkit/fast pcmkit/e2e pcmkit/oracle
python3 -m ruff format --check pcmkit/fast pcmkit/e2e pcmkit/oracle
python3 -m mypy pcmkit/fast pcmkit/e2e pcmkit/oracle
