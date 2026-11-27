# routemap

The county's school bus network in Neo4j 5.26: stops, routes, schools and depots.

- `bin/rq <target> "<cypher>"` or `bin/rq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml` through the transport team's query gateway (it holds the credentials).
- `changes/`: reviewed changes to `live`, `NNNN-<what>.cypher`.
- `fixtures/dev-seed.cypher`: what `dev` is rebuilt from.
- `docs/targets.md`: the targets. `docs/model.md`: the graph.
