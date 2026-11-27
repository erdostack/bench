# colonyreg

The Calder Moor Beekeepers' Association colony register, as a graph in SQLite: apiaries, colonies and the
members who keep them, in `nodes`, and what links them in `edges`. The swarm line, the inspection app and
the apiary map use it.

- `bin/rq <target> "<sql>"` or `bin/rq <target> --file <file.sql>`: run SQL on a target from `targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a data change (calls its `run(conn)`).
- `changes/`: data changes, one file each. `tickets/`: copies of the tickets we work from.
- `db/schema.sql`: the schema. `docs/`: targets, changes, the model, colony movements.
