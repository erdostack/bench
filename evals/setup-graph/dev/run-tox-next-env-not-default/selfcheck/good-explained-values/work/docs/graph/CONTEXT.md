# Graph context

## Facts

engine: Memgraph (throwaway Testcontainers container)
engine_version: 3.4.0 (container.py default; only tox -e next overrides it)
query_language: Cypher
driver: neo4j (Python driver) 5.28.1
run_queries: tox -e adhoc -- queries/swap_chains.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: shiftswap/container.py defaults MEMGRAPH_IMAGE to memgraph/memgraph:3.4.0; tox.ini's [testenv] and [testenv:adhoc] do not set it; README.md agrees
- driver: requirements.txt pins neo4j==5.28.1 (testcontainers 4.9.0 starts the container)
- run_queries: tox -e adhoc runs python -m shiftswap.adhoc
- access: nothing authorises writes

## Open questions

- None.
