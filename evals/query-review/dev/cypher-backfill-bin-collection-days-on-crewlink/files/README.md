# binroutes

The district's waste collection rounds as a Neo4j 5.26 graph: properties, their bins, and the rounds the
bins are collected on (`docs/model.md`).

- `bin/cl <target> "<cypher>"` or `bin/cl <target> --file <file>`: run Cypher on a target from `config/targets.toml`.
- `changes/`: data changes, `NNNN_<what>.cypher`.
- `docs/targets.md`: the targets and how changes are made.
