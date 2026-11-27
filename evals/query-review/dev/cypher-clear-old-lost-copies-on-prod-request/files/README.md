# branchline-catalogue-ops

Operational Cypher for the Branchline libraries catalogue graph (titles, copies, branches, patrons).

- `bin/lq <target> "<cypher>"` or `bin/lq <target> --file <file>`: run Cypher on a target from
  `config/targets.toml`.
- `ops/`: one file per change made to production data, `<yyyy-mm-dd>-<what>.cypher`.
- `queries/`: read-only reports.
- `docs/`: the model and the rules for production.
