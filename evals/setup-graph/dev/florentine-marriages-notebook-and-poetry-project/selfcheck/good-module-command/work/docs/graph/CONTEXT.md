# Graph context

## Facts

engine: NetworkX (in-memory graph from a CSV)
engine_version: 3.3 (poetry.lock)
query_language: none (Python; NetworkX API)
driver: networkx 3.3
run_queries: poetry run python -m medici.ask path Medici Strozzi
access: read-only
schema_snapshot: none

## Evidence

- engine: medici/graph.py builds a NetworkX graph from data/marriages.csv
- engine_version: poetry.lock pins networkx 3.3 (pyproject.toml: ^3.1)
- run_queries: Makefile target ask -> poetry run python -m medici.ask

## Open questions

- Notebook pins networkx==3.1 in its install cell; project lock is 3.3.
