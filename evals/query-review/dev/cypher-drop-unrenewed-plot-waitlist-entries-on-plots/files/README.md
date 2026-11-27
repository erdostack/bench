# plotgraph

Allotment lettings for the Greenfinch Seed Exchange and Allotment Society: sites, plots, tenants and the
waiting lists, in Neo4j 5.26.

- `bin/aq <target> "<cypher>"` or `bin/aq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml` through the society's query gateway (it holds the credentials).
- `changes/`: reviewed data changes, `NNN-<what>.cypher`.
- `docs/targets.md`: targets and how data changes are made. `docs/model.md`: the graph.
  `docs/waiting-list.md`: how the waiting lists work.
