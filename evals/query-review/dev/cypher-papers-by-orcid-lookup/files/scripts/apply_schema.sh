#!/usr/bin/env bash
# Apply every schema file in order. Needs cypher-shell and NEO4J_URI / NEO4J_USERNAME / NEO4J_PASSWORD.
set -euo pipefail
for f in "$(dirname "$0")"/../schema/*.cypher; do
  echo "applying $f"
  cypher-shell -a "$NEO4J_URI" -u "$NEO4J_USERNAME" -p "$NEO4J_PASSWORD" --file "$f"
done
