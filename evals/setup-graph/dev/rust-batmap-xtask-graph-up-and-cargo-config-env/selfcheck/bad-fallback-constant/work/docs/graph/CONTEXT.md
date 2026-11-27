# Graph context

## Facts

engine: neo4j
engine_version: 5.26.24
query_language: Cypher
driver: neo4rs 0.8.0
run_queries: cargo run -q -p batq -- queries/cut_off_by.cypher
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- driver: Cargo.lock resolves neo4rs 0.8.0
- run_queries: README.md and the xtask q subcommand
- credentials: graph.env (not copied)

## Open questions

- None.
