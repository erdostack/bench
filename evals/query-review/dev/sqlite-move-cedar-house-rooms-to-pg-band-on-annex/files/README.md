# residencegraph

Blocks, rooms and residents of the university's residences, as node and edge tables in SQLite.

- `bin/resq <target> "<sql>"` or `bin/resq <target> --file <file.sql>`: run SQL on a target from
  `config/targets.toml`.
- `ops/`: reviewed changes to production data. See `docs/ENVIRONMENTS.md`.
- `docs/model.md`: node kinds, edge types and bands.
