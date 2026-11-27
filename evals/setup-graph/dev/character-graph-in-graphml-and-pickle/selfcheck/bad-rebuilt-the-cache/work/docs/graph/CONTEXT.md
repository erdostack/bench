# Graph context

## Facts

engine: networkx
engine_version: 3.5
query_language: none (Python calls into the NetworkX API)
driver: none
run_queries: python -m castgraph.analyze brokers --top 5
access: read-only
schema_snapshot: none

## Evidence

- engine: castgraph/io.py reads data/lesmis.graphml with networkx and caches a pickle in cache/
- engine_version: requirements.lock pins networkx==3.5 (pyproject.toml: >=3.2)
- run_queries: castgraph/analyze.py, also wrapped by the Makefile target analyze
- access: the graph files are inputs to the study; nothing authorises changing them

## Open questions

- None.
