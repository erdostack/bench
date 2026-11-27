# fenland-donors

Donors, centres and recruitment campaigns of the Fenland Blood Service as a graph in `nodes` and `edges`
(SQLite).

- `bin/fb <target> "<sql>"` or `bin/fb <target> --file <file.sql>`: run SQL on a target from
  `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`, `db/schema.sql`, `docs/`.
