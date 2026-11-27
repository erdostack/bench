# accessgraph-ops

Operational Cypher for the access graph (principals, groups, applications).

- `bin/gq <target> "<cypher>"` or `bin/gq <target> --file <file>`: run Cypher on a target from
  `config/targets.toml`. Every call is logged to `.gq_history` before it runs.
- `ops/`: one file per change to production data, `<yyyy-mm-dd>-<what>.cypher`.
- `queries/`: read-only diagnostics.
- `docs/`: the rules for production, tickets.
