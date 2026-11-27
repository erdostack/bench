# fedgraph

The chess federation's graph: players, clubs, events and who entered what. Neo4j 5.26 Enterprise on
every target, no plugins (APOC is not installed).

- `bin/rq <target> "<cypher>"` or `bin/rq <target> --file <file>`: run Cypher on a target from `config/targets.toml`.
- `changes/`: reviewed data changes, `<yyyymmdd>-<what>.cypher`.
- `docs/graph.md`: the model and property types. `docs/targets.md`: the targets and how changes are made.
