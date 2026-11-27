# wyvern-donor-graph

The donor graph of the Wyvern Blood Service in Neo4j: donors, donation sessions and venues, appointments,
and the reminders we send. The booking site, the session planners and the reminder sender query it.

- `bin/vq <target> "<cypher>"` or `bin/vq <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: one file per change to data, `NNN_<what>.cypher`.
- `docs/environments.md`, `docs/changes.md`, `docs/model.md`, `docs/retention.md`.
