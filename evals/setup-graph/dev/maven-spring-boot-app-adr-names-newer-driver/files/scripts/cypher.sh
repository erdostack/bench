#!/usr/bin/env bash
# scripts/cypher.sh <file.cypher>: run a query file with cypher-shell inside the compose container, read access.
set -euo pipefail
file="${1:?usage: scripts/cypher.sh <file.cypher>}"
docker compose exec -T graph cypher-shell --access-mode read -u neo4j \
  -p "${SHELFMARK_DB_PASSWORD:-localdev}" < "$file"
