# Graph context

## Facts

engine: networkx
engine_version: >=3.1
query_language: none (Python calls into NetworkX)
driver: none
run_queries: uv run python -m clubnet.cli factions
access: read-only
schema_snapshot: none

## Evidence

- engine: clubnet/load.py reads data/ties.edgelist and data/members.csv with networkx; no database
- engine_version: uv.lock pins networkx 3.4.2 (pyproject.toml: >=3.1)
- run_queries: README.md and clubnet/cli.py
- access: README calls the data read-only course material

## Open questions

- README.md says NetworkX 3.2, but uv.lock installs 3.4.2. The README line looks stale.
