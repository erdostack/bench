# Graph context

## Facts

engine: Neo4j 5.26 LTS (Community, Docker)
engine_version: 5.26.14
query_language: Cypher (v5)
driver: neo4j-go-driver v5.28.1
run_queries: go run ./cmd/crewq -f queries/crew_for_role.cypher -p production=prod-007
access: read-only
schema_snapshot: none

## Evidence

- engine / engine_version: compose.yaml runs neo4j:5.26.14-community; README.md says the same
- driver: go.mod requires neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q -> go run ./cmd/crewq (readers routing)
- access: crewq reads only; make load is the scheduling leads' job
- credentials: NEO4J_AUTH is in .env (not copied here)

## Open questions

- None.
