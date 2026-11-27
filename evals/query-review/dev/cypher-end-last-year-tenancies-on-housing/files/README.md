# housing-graph

Student housing as a graph: residences, rooms, students and their tenancies, in Neo4j.

- `bin/tq <target> "<cypher>"` or `bin/tq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: one file per change to data, `NNN-<what>.cypher`.
- `docs/DATA.md`: where the data lives and how it is changed. `docs/model.md`: the graph.
