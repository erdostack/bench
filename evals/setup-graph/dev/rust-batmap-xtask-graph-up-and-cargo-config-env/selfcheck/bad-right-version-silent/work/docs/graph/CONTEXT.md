# Graph context

## Facts

engine: neo4j
engine_version: 2026.05.0
query_language: Cypher
driver: neo4rs 0.8.0
run_queries: cargo run -q -p batq -- queries/cut_off_by.cypher
access: read-only
schema_snapshot: schema/constraints.cypher

## Evidence

- engine_version: .cargo/config.toml [env] BATMAP_NEO4J_TAG
- driver: Cargo.lock resolves neo4rs 0.8.0
- run_queries: README.md and the xtask q subcommand
- credentials: graph.env (not copied)

## Open questions

- None.
