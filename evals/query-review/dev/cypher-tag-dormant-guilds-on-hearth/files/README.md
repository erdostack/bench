# hearth-graph

The social graph behind Emberfall's guilds, friends and the guild finder. Neo4j 5.26 Enterprise on every
target.

- `bin/hq <target> "<cypher>"` or `bin/hq <target> --file <file>`: run Cypher on a target in
  `config/targets.toml` (cypher-shell, auto-commit).
- `changes/NNNN_<what>.cypher`: reviewed data changes.
- `docs/model.md`: the graph. `docs/targets.md`: the targets and how changes are run.
