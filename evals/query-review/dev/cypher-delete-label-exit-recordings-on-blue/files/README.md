# tonearm-graph

Cypher and tooling for the Tonearm music catalogue graph: artists, recordings, releases, labels, and
the listener signals the recommendation jobs read.

- `bin/mq <target> "<cypher>"` or `bin/mq <target> --file <file>`: send Cypher to a target from
  `config/targets.toml`.
- `db/changes/`: data and schema changes, `NNNN_<what>.cypher`, run in number order.
- `queries/`: read-only Cypher used by the jobs.
- `docs/`: the model, the deployment, and how changes are made.
