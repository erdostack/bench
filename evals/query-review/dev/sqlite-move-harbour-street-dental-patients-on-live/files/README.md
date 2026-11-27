# practicegraph

Brightwater Dental Group's practices, clinicians, patients and courses of treatment, as a graph in
SQLite (`nodes`, `edges`). Reception, the clinicians' day lists and the claims run read it.

- `bin/dq <target> "<sql>"` (or `--file <file.sql>`): run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a data change (see `docs/changes.md`).
- `changes/`: data changes, one `.sql` file each. `db/schema.sql`: the schema.
- `docs/`: environments, changes, practices.
