# smilegraph

Brightwater Dental Group's patient graph in Neo4j 5.26: the group's practices, patients, their recall
schedule and the reminders sent about it.

- `bin/cs <target> "<cypher>"` or `bin/cs <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml` (the gateway holds the credentials).
- `changes/`: reviewed data changes, `NNNN-<what>.cypher`.
- `docs/environments.md`: targets and the rules for changing data. `docs/graph.md`: the model.
