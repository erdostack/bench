# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher
driver: github.com/neo4j/neo4j-go-driver/v5 v5.28.1
run_queries: make q F=queries/isolated_by_section.cypher SECTION=S-0412
access: read-only
schema_snapshot: none

## Evidence

- engine_version: deploy/graph/compose.yaml image line, README.md

## Open questions

- none
