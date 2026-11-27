# Graph context

## Facts

engine: networkx
engine_version: 3.2.1
query_language: none (Python, NetworkX bipartite API)
driver: networkx 3.2.1
run_queries: make project
access: read-only
schema_snapshot: none

## Evidence

- engine: attend/graph.py builds a bipartite NetworkX graph from data/attendance.csv; nothing is persisted
- engine_version: requirements.txt (pip-compile output, installed with --require-hashes in CI) pins networkx==3.2.1; requirements.in says ~=3.2
- run_queries: scripts/run.sh -> python -m attend.cli

## Open questions

- docs/design.md says the project uses NetworkX 3.4, but the compiled requirements install 3.2.1. Either the doc is ahead of the lock or the lock needs recompiling.
