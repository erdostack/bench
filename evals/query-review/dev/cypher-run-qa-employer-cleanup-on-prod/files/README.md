# jobgrid-graph-ops

Operational Cypher for the Jobgrid graph (employers, jobs, candidates, applications). Neo4j 5.26 on
every target.

- `bin/kq <target> "<cypher>"` or `bin/kq <target> --file <file>`: run Cypher on a target from
  `config/targets.toml` (cypher-shell). Every call is logged to `.kq_history`.
- `ops/`: one file per change to production data, `<yyyy-mm-dd>-<what>.cypher`.
- `queries/`: read-only checks.
