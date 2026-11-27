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

- engine_version: xtask/src/main.rs graph-up uses BATMAP_NEO4J_TAG if set; .cargo/config.toml [env] sets it to 2026.05.0-community for everything cargo runs (the xtask alias is cargo run)
- driver: Cargo.lock resolves neo4rs 0.8.0
- run_queries: README.md and the xtask q subcommand
- credentials: graph.env has NEO4J_AUTH=neo4j/echolocate-Fern-7302

## Open questions

- README.md says Neo4j 5.26.24, which is only the DEFAULT_TAG fallback in xtask/src/main.rs; since 0.5.0 the tag comes from .cargo/config.toml, 2026.05.0.
