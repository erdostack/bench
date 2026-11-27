# Graph context

## Facts

engine: networkx
engine_version: 3.3
query_language: none (Python; NetworkX API)
driver: none
run_queries: make ask Q=brokers
access: read-only
schema_snapshot: none

## Evidence

- engine: medici/graph.py builds a NetworkX graph from data/marriages.csv
- engine_version: poetry.lock pins networkx 3.3 (pyproject.toml: ^3.1)
- run_queries: Makefile target ask -> poetry run python -m medici.ask

## Open questions

- notebooks/explore.ipynb starts with `%pip install networkx==3.1`, which installs a different NetworkX (3.1) into the kernel than the project's lock (3.3). The notebook and the CLI can therefore run different versions.
