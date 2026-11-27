#!/usr/bin/env bash
# scripts/q.sh <file.cypher>: run a saved query through the read-only runner.
set -euo pipefail
file="${1:?usage: scripts/q.sh <file.cypher>}"
cd "$(dirname "$0")/.."
exec uv run python -m ferryboard.tools.runq "$file"
