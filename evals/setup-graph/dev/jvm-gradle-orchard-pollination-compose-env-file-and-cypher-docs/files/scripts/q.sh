#!/usr/bin/env sh
# scripts/q.sh <file.cypher>: run one read query against the local graph.
set -eu
[ $# -eq 1 ] || { echo "usage: scripts/q.sh <file.cypher>" >&2; exit 2; }
export ORCHARD_PASSWORD="$(sed -n 's#^NEO4J_AUTH=neo4j/##p' graph.env)"
exec ./gradlew -q run --args="$1"
