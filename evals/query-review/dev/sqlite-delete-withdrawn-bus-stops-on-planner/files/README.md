# schoolrun

Home-to-school transport for the county's 41 schools as a graph: stops, routes, schools, students and
vehicles in `nodes`, and what links them in `edges`. SQLite.

- `bin/sq <target> "<sql>"` or `bin/sq <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each, `NNNN_<what>.py`.
- `db/schema.sql`: the schema. `docs/targets.md`: the targets and how data changes are made. `docs/model.md`: node and edge kinds.
