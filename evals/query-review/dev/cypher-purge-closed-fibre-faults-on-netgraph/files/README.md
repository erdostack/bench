# westmoor-graph

The network graph of Westmoor Community Broadband in Neo4j: cabinets, premises, faults and the engineers
who work them. The fault desk and the field app query it.

- `bin/wq <target> "<cypher>"` or `bin/wq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: one file per change to data, `NNN-<what>.cypher`.
- `docs/environments.md`, `docs/changes.md`, `docs/model.md`.
