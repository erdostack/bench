#!/usr/bin/env bash
# scripts/mgq.sh <file.cypher>: pipe a saved query into the console client inside the container.
set -euo pipefail
docker compose exec -T graph mgconsole --output-format=csv < "${1:?usage: scripts/mgq.sh <file.cypher>}"
