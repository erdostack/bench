#!/usr/bin/env bash
# scripts/run_query.sh <file.cypher>: read-only query runner.
set -euo pipefail
cd "$(dirname "$0")/.."
exec python -m orchard.tools.run_query "${1:?usage: scripts/run_query.sh <file.cypher>}"
