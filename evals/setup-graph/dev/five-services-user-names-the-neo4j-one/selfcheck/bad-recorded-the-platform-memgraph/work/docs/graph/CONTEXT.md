# Graph context

## Facts

engine: Memgraph
engine_version: 3.5.0
query_language: Cypher
driver: pymgclient 1.4.0
run_queries: make mgq FILE=services/routing/queries/next_hop.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: README.md (Graph database) and compose.yaml; docs/architecture.md says lineage shares the Memgraph instance
- driver: services/routing/requirements.txt
- run_queries: Makefile target mgq

## Open questions

- None.
