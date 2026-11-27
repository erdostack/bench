# Graph context

## Facts

engine: postgres (PostgreSQL + Apache AGE)
engine_version: 16.6 (AGE 1.5.0)
query_language: Cypher through AGE's cypher() SQL function
driver: github.com/jackc/pgx/v5 v5.7.2
run_queries: make q F=queries/most_cited.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: compose files
- driver: go.mod
- run_queries: Makefile

## Open questions

- None.
