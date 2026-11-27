#!/usr/bin/env bash
# scripts/run-query.sh <file.cypher>: run one saved query against the compose graph, read-only.
set -euo pipefail
cd "$(dirname "$0")/.."
exec ./mvnw -q -pl app exec:java -Dexec.args="${1:?usage: scripts/run-query.sh <file.cypher>}"
