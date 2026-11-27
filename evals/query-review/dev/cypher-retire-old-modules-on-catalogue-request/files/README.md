# modulegraph

The university's module catalogue as a graph: modules, the programmes they belong to and the
prerequisites between them, in Neo4j.

- `bin/modq <target> "<cypher>"` or `bin/modq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: one file per change to production data, `<ticket>-<what>.cypher`.
- `docs/RUNBOOK.md`: targets and how data changes. `docs/model.md`: the graph.
