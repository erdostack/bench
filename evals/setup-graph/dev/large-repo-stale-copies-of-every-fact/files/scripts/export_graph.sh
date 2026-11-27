#!/usr/bin/env bash
# scripts/export_graph.sh: write a dump of the development database to var/dumps/ (the server stops while it runs).
set -euo pipefail
cd "$(dirname "$0")/.."
compose="docker compose -f ops/compose/graph.yaml"
mkdir -p var/dumps
$compose stop graph
$compose run --rm -v "$PWD/var/dumps:/dumps" graph neo4j-admin database dump neo4j --to-path=/dumps --overwrite-destination=true
$compose up -d graph
