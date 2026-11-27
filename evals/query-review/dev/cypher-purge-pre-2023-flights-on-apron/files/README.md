# aodb-graph

The airport operational database's flight graph: every flight, where it parked, which gate it used,
which runway, who operated it and which arrival turned into which departure. Neo4j 5.26 Enterprise on
every target.

- `bin/aq <target> "<cypher>"` or `bin/aq <target> --file <file>`: run Cypher on a target in
  `config/targets.toml`.
- `changes/`: reviewed data changes, `AODB-<ticket>-<slug>.cypher`.
- `docs/model.md`: the graph. `docs/targets.md`: the targets and how changes reach them.
