#!/usr/bin/env bash
# scripts/mgq.sh <file.cypher>: run a Cypher file against the shared Memgraph.
set -euo pipefail
file="${1:?usage: scripts/mgq.sh <file.cypher>}"
root="$(cd "$(dirname "$0")/../../.." && pwd)"
docker compose -f "$root/compose.yaml" exec -T memgraph mgconsole < "$file"
