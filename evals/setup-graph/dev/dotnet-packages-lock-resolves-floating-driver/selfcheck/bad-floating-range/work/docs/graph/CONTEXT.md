# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: Neo4j.Driver 5.*
run_queries: make q F=queries/coverage_gaps.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml image neo4j:2026.05.0-enterprise
- driver: src/ChargeMap.Query/packages.lock.json (csproj Version="5.*", CI restores --locked-mode)
- run_queries: Makefile target q
- credentials: .env (not copied)

## Open questions

- README.md says Neo4j.Driver 5.21.0; the lock file resolves 5.28.1.
