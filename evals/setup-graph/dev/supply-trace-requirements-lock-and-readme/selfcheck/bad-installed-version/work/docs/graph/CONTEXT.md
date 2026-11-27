# Graph context

## Facts

engine: networkx
engine_version: 3.7
query_language: none (Python, NetworkX DiGraph)
driver: networkx 3.7
run_queries: make trace SKU=C-0107
access: read-only
schema_snapshot: none

## Evidence

- engine: supplytrace/trace.py loads data/supply.csv into a NetworkX DiGraph
- engine_version: requirements.lock pins networkx==3.5 (installed by make deps); README.md says the same
- run_queries: Makefile target trace

## Open questions

- README.md says 3.5 but the installed NetworkX is 3.7; the README is stale.
