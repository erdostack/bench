# gridops-graph

Operational Cypher for the network graph (substations, feeders, transformers, service points, meters).

- `bin/gq <target> "<cypher>"` or `bin/gq <target> --file <file>`: run Cypher on a target from `config/targets.toml`.
- `ops/`: one file per change made to production data, `<yyyy-mm-dd>-<what>.cypher`.
- `queries/`: read-only diagnostics.
- `docs/`: model, sizes and the rules for production.
