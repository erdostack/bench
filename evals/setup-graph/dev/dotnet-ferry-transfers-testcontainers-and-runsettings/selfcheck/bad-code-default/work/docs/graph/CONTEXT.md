# Graph context

## Facts

engine: Neo4j (throwaway Testcontainers container)
engine_version: 5.26.24
query_language: Cypher
driver: Neo4j.Driver 5.28.1
run_queries: make q F=queries/transfers.cypher
access: read-only
schema_snapshot: none

## Evidence

- driver: Directory.Packages.props and tests/Ferry.Graph.Tests/packages.lock.json
- run_queries: Makefile target q

## Open questions

- none
