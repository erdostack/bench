# Graph context

## Facts

engine: Neo4j Community (Docker, started by cargo xtask graph-up)
engine_version: 2026.05.0-community
query_language: Cypher
driver: neo4rs 0.8.0
run_queries: cargo xtask q queries/busiest_corridors.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine_version: xtask/src/main.rs graph-up uses BATMAP_NEO4J_TAG if set; .cargo/config.toml [env] sets it to 2026.05.0-community for everything cargo runs (the xtask alias is cargo run)
- driver: Cargo.lock resolves neo4rs 0.8.0
- run_queries: README.md and the xtask q subcommand
- credentials: graph.env (not copied)

## Open questions

- README.md says Neo4j 5.26.24, which is only the DEFAULT_TAG fallback in xtask/src/main.rs; since 0.5.0 the tag comes from .cargo/config.toml, 2026.05.0.
