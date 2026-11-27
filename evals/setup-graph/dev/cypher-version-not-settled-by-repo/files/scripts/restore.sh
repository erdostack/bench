#!/usr/bin/env bash
# scripts/restore.sh <dump file>: replace the local catalogue with the given dump.
set -euo pipefail
dump="${1:?usage: npm run restore -- dumps/<file>.dump}"
[ -f "$dump" ] || { echo "no such file: $dump" >&2; exit 1; }

docker compose stop graph
docker compose run --rm --no-deps graph \
  neo4j-admin database load neo4j --from-path=/dumps --overwrite-destination=true
docker compose up -d graph
echo "restored $(basename "$dump"); the server may take a minute to come back"
