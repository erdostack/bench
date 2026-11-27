# seedstore

The co-op's seed catalogue as a Neo4j graph: seed lots, the varieties they are, and members' reservations
(`docs/model.md`). The ordering site and the branch tills read it.

- `bin/sq <target> "<cypher>"` or `bin/sq <target> --file <file>`: send Cypher to a target from
  `config/targets.toml`. Every call is logged to `.sq_history` first.
- `changes/`: data changes, `NNNN_<what>.cypher`. See `docs/targets.md`.
