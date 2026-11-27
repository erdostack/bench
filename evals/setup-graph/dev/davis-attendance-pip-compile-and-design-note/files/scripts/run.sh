#!/usr/bin/env sh
# scripts/run.sh project <women|events> | cores
set -eu
cd "$(dirname "$0")/.."
exec python -m attend.cli "$@"
