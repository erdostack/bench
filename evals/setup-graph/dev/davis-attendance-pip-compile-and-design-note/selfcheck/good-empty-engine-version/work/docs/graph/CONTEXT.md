# Graph context

## Facts

engine: NetworkX, in process (CSV rebuilt each run)
engine_version: networkx 3.2.1 (library, not a database)
query_language: none (Python, NetworkX bipartite API)
driver: networkx 3.2.1 (requirements.txt)
run_queries: python -m attend.cli cores
access: read-only
schema_snapshot: none

## Evidence

- engine: attend/graph.py builds a bipartite NetworkX graph from data/attendance.csv; nothing is persisted
- engine_version: requirements.txt (pip-compile output, installed with --require-hashes in CI) pins networkx==3.2.1; requirements.in says ~=3.2
- run_queries: scripts/run.sh -> python -m attend.cli

## Open questions

- Design doc: NetworkX 3.4. requirements.txt: 3.2.1. Stale doc or stale lock.
