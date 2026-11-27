# seedbank

Stock records of the Greenfinch Seed Exchange and Allotment Society as a graph: members, varieties, seed
packets and the stores they sit in. SQLite, `nodes` and `edges`.

- `bin/gq <target> "<sql>"` or `bin/gq <target> --file <file.sql>`: run SQL on a target in `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file (see `docs/operations.md`).
- `changes/`: data changes, `NNN-<slug>.sql`.
- `docs/model.md`: node and edge kinds. `docs/operations.md`: targets and how changes are made.
