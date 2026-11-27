# fleetwatch

Live positions of the county's school buses, as a graph in Neo4j 5.26: buses, stops and the GPS pings
that link them.

- `bin/dq <target> "<cypher>"` or `bin/dq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml` (the gateway holds the credentials).
- `changes/`: reviewed data changes, `NNNN-<what>.cypher`.
- `docs/environments.md`: targets and the rules for changing data. `docs/graph.md`: the model.
