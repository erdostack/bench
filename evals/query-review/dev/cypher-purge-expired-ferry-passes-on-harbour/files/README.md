# skerrow-graph

The booking graph of Skerrow Island Ferries in Neo4j: customers, their season and multi-trip passes, routes,
sailings, and every boarding scanned at the ramps.

- `bin/sk <target> "<cypher>"` or `bin/sk <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: one file per data change, `NNN-<what>.cypher`.
- `docs/environments.md`, `docs/changes.md`, `docs/model.md`.
