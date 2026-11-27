# upperdale-fibre

The build and service graph of Upper Dale Fibre, a community fibre build across eleven hill villages:
premises, the cabinets they sit behind, and where each premises is in the build. In Neo4j.

- `bin/ud <target> "<cypher>"` or `bin/ud <target> --file <file.cypher>`: send Cypher to a target.
- `config/targets.toml`: the targets. `docs/targets.md`: what they are.
- `changes/`: data changes, `NNN_<what>.cypher`. `docs/changes.md`: how they are made.
- `docs/model.md`: the graph.
