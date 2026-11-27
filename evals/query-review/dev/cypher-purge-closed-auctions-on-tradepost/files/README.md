# auction-house

Graph behind the Emberfall auction house: auctions, the items on them, sellers and bids. Neo4j 5.26 on
every target.

- `bin/tpq <target> "<cypher>"` or `bin/tpq <target> --file <file>`: run Cypher on a target from
  `targets.toml`.
- `changes/<yyyy-mm-dd>-<what>.cypher`: data changes, reviewed.
- `docs/graph.md`: the model. `docs/environments.md`: targets and the rules for writes.
