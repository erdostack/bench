# Graph context

## Facts

engine: Kuzu (embedded, packages/fitment)
engine_version: ^0.10.0
query_language: Cypher
driver: kuzu ^0.10.0
run_queries: pnpm fit:q queries/fits_frame.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: packages/fitment
- run_queries: package.json

## Open questions

- None.
