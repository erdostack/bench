# Graph context

## Facts

engine: Kuzu (embedded)
engine_version: 0.11.2 (kuzu package, yarn.lock)
query_language: Cypher
driver: kuzu (npm) 0.11.2
run_queries: node bin/q.mjs queries/co_sighted.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine: bin/q.mjs opens db/survey.kuzu with the kuzu npm package in process (embedded, no server)
- engine_version / driver: yarn.lock resolves kuzu@npm:^0.11.0 to 0.11.2 (package.json ^0.11.0; packageManager yarn@4.5.3)
- run_queries: package.json script q -> node bin/q.mjs (opens the database read-only)
- schema_snapshot: schema.cypher

## Open questions

- README: 0.11.1. Lock: 0.11.2.
