# Graph context

## Facts

engine: neo4j
engine_version: 5.26
query_language: Cypher 5
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/worked_together.cypher P=pers-0042
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine / engine_version: compose.yaml runs neo4j:5.26.14-community; README.md says the same
- driver: go.mod requires neo4j-go-driver/v5 v5.28.1
- run_queries: Makefile target q -> go run ./cmd/crewq (readers routing)
- access: crewq reads only; make load is the scheduling leads' job
- credentials: NEO4J_AUTH is in .env (not copied here)

## Open questions

- None. The saved queries use CALL (x) { } subqueries, which need 5.23+; the server is 5.26.14, so that is fine.
