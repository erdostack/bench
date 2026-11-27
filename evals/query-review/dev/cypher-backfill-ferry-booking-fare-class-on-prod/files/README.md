# kelda-bookings

Kelda Sound Ferries' booking graph in Neo4j: accounts, bookings and the sailings they are on. The booking
site, the ticket office, the port gates and finance's reports use it.

- `bin/kf <target> "<cypher>"` or `bin/kf <target> --file <file.cypher>`: send Cypher to a target in
  `config/targets.toml`.
- `changes/`: data changes, `NNN-<what>.cypher`, one file each.
- `docs/environment.md`: the database and how changes are made. `docs/model.md`: the model.
  `docs/fares.md`: fare classes.
