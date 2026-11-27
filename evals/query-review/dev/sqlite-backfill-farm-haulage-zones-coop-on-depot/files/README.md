# fieldline

The co-operative's trading graph: member farms, grain stores, haulage zones and the edges between them.
Kept in SQLite node and edge tables (`db/schema.sql`).

- `bin/dq <target> "<sql>"` or `bin/dq <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each.
- `docs/targets.md`: the targets and how a change reaches them. `docs/model.md`, `docs/haulage.md`: the model.
