# workgraph

Work orders on the water distribution network's assets (hydrants, valves, mains), stored as a Neo4j graph
(`docs/model.md`).

- `bin/wg <target> "<cypher>"` or `bin/wg <target> --file <file>`: send Cypher to a target from
  `config/targets.toml`. Every call is logged to `.wg_history` first.
- `changes/`: data changes, `NNN-<what>.cypher`.
- `docs/targets.md`: the targets and how changes are made. `docs/archiving.md`: what archiving an order means.
