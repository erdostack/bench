# Graph context

## Facts

engine: Memgraph (graph-next service; spoken to through the neo4rs Bolt client)
engine_version: 3.5.1
query_language: Cypher
driver: neo4rs 0.8.0
run_queries: cargo run --quiet --bin lendq -- queries/overdue.cypher
access: read-only
schema_snapshot: none

## Evidence

- engine and engine_version: .devcontainer/devcontainer.json starts runServices workspace and graph-next and sets GRAPH_URI=bolt://graph-next:7687; compose.yaml gives graph-next memgraph/memgraph:3.5.1
- driver: Cargo.lock resolves neo4rs 0.8.0
- run_queries: Makefile target q runs cargo run --bin lendq

## Open questions

- README.md says Memgraph 2.21 (the graph service), but since 0.6.0 (CHANGELOG.md) the dev container runs graph-next on 3.5.1; graph (2.21.1) only starts with the legacy-export profile.
