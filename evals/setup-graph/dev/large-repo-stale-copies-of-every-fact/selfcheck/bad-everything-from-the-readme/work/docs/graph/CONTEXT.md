# Graph context

## Facts

engine: neo4j
engine_version: 5.20
query_language: Cypher
driver: neo4j 5.23.1
run_queries: ./scripts/run_query.sh queries/on_loan_now.cypher
access: read-only
schema_snapshot: db/schema.cypher

## Evidence

- engine_version, run_queries, schema_snapshot: README.md
- driver: requirements-dev.txt

## Open questions

- None.
