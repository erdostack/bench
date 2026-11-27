# ridegraph

The bike-share scheme's members, bikes, stations and rides as a Neo4j graph. The rider app, the fare
engine and the rebalancing vans work off it.

- `bin/rg <target> "<cypher>"` / `bin/rg <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `changes/`: reviewed data changes, `NNNN-<slug>.cypher`.
- `queries/`: saved read queries.
- `docs/`: targets, model, retention.
