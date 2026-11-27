# Graph context

## Facts

engine: memgraph
engine_version: 4.9.0
query_language: Cypher
driver: neo4j 5.28.1
run_queries: tox -e adhoc -- queries/longest_journeys.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: tox.ini [testenv] sets MEMGRAPH_IMAGE = memgraph/memgraph:3.4.0, inherited by [testenv:adhoc]; ringnet/container.py only falls back to 2.21.0 when the variable is unset
- driver: requirements.txt pins neo4j==5.28.1 (testcontainers 4.9.0 starts the container)
- run_queries: tox -e adhoc runs python -m ringnet.adhoc
- access: nothing authorises writes

## Open questions

- README.md says Memgraph 2.21.0 (the code default), but tox always sets MEMGRAPH_IMAGE to 3.4.0. Running ringnet.adhoc outside tox would start 2.21.0.
