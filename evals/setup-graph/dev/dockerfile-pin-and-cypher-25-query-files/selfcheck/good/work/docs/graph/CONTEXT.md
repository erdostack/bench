# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher 5
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make cypher F=queries/self_citations.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose.yaml builds docker/graph, whose Dockerfile is FROM neo4j:5.26.24-community (CHANGELOG 2026-07-14: back on 5.26 LTS)
- driver: go.mod
- run_queries: Makefile target cypher (cmd/cq)

## Open questions

- README.md says Neo4j 2026.05 with Cypher 25, but the image is 5.26.24 since the 2026-07-14 roll-back. A 5.26 server only runs Cypher 5, so the `CYPHER 25` prefix in every file under queries/ will make them fail; the prefixes (and any Cypher 25-only syntax) need to come out, or the image has to move forward again.
