#!/usr/bin/env bash
# scripts/q.sh <file.cypher> [name=value ...]: run a saved query read-only.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python -m gridwatch.cli query "$@"
