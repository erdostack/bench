# campusgraph

The students' union and university's shared graph of students, programmes, societies and sports clubs,
in Neo4j.

- `bin/cq <target> "<cypher>"` or `bin/cq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: one file per change to production data, `YYYY-MM-DD-<what>.cypher`.
- `docs/RUNBOOK.md`: the targets and how data is changed. `docs/model.md`: the graph.
