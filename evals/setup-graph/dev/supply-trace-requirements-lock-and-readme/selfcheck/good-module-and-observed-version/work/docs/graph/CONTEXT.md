# Graph context

## Facts

engine: NetworkX (DiGraph over data/supply.csv)
engine_version: 3.5 (requirements.lock; 3.7 is what this machine has installed)
query_language: none (Python, NetworkX DiGraph)
driver: none
run_queries: python -m supplytrace.trace C-0110
access: read-only
schema_snapshot: none

## Evidence

- engine: supplytrace/trace.py loads data/supply.csv into a NetworkX DiGraph
- engine_version: requirements.lock pins networkx==3.5 (installed by make deps); README.md says the same
- run_queries: Makefile target trace

## Open questions

- None.
