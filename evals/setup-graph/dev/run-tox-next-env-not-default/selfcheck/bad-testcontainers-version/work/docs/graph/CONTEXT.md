# Graph context

## Facts

engine: memgraph
engine_version: 4.9.0
query_language: Cypher
driver: neo4j 5.28.1
run_queries: tox -e adhoc -- queries/swap_chains.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: shiftswap/container.py defaults MEMGRAPH_IMAGE to memgraph/memgraph:3.4.0; tox.ini's [testenv] and [testenv:adhoc] do not set it; README.md agrees
- driver: requirements.txt pins neo4j==5.28.1 (testcontainers 4.9.0 starts the container)
- run_queries: tox -e adhoc runs python -m shiftswap.adhoc
- access: nothing authorises writes

## Open questions

- `tox -e next` runs the tests on Memgraph 3.5.0; queries written now should still run on 3.4.0.
