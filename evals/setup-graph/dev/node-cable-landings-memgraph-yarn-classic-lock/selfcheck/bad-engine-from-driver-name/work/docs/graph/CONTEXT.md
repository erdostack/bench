# Graph context

## Facts

engine: neo4j
engine_version: unknown
query_language: Cypher (Memgraph dialect)
driver: neo4j-driver 5.28.1
run_queries: yarn q queries/redundancy.cypher country=PT
access: read-only
schema_snapshot: none

## Evidence

- engine / engine_version: compose.yaml runs memgraph/memgraph:3.2.0 (the neo4j-driver package is only the Bolt client)
- driver: yarn.lock resolves neo4j-driver@^5.12.0 to 5.28.1; package.json packageManager is yarn@1.22.22
- run_queries: package.json script q -> node bin/q.mjs (READ sessions)
- access: README.md says the repo only reads

## Open questions

- README.md says neo4j-driver 5.12.2; yarn.lock installs 5.28.1.
