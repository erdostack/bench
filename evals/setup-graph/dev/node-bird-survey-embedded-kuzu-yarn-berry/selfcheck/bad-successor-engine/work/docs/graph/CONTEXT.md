# Graph context

## Facts

engine: ladybug
engine_version: 0.11.2
query_language: Cypher
driver: kuzu 0.11.2
run_queries: yarn q queries/co_sighted.cypher
access: read-only
schema_snapshot: schema.cypher

## Evidence

- engine: bin/q.mjs opens db/survey.kuzu with the kuzu npm package in process (embedded, no server)
- engine_version / driver: yarn.lock resolves kuzu@npm:^0.11.0 to 0.11.2 (package.json ^0.11.0; packageManager yarn@4.5.3)
- run_queries: package.json script q -> node bin/q.mjs (opens the database read-only)
- schema_snapshot: schema.cypher

## Open questions

- README.md says Kuzu 0.11.1; yarn.lock installs 0.11.2.
