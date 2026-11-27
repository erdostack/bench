# coursegraph

The school's course graph: students, modules and staff, with who takes, teaches and advises what.
SQLite, as node and edge tables.

- `bin/cgq <target> "<sql>"` or `bin/cgq <target> --file <file.sql>`: run SQL on a target from
  `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (used for `records`).
- `docs/targets.md`: the targets. `docs/model.md`: node kinds and edge types.
