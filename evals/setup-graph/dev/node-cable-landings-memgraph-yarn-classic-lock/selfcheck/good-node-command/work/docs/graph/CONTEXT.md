# Graph context

## Facts

engine: Memgraph (queried over Bolt with neo4j-driver)
engine_version: 3.2.0
query_language: Cypher
driver: neo4j-driver 5.28.1 (yarn.lock)
run_queries: node bin/q.mjs queries/two_cable_path.cypher from=PT
access: read-only
schema_snapshot: none

## Evidence

- engine / engine_version: compose.yaml runs memgraph/memgraph:3.2.0 (the neo4j-driver package is only the Bolt client)
- driver: yarn.lock resolves neo4j-driver@^5.12.0 to 5.28.1; package.json packageManager is yarn@1.22.22
- run_queries: package.json script q -> node bin/q.mjs (READ sessions)
- access: README.md says the repo only reads

## Open questions

- Driver: README 5.12.2 vs lock 5.28.1.
