# hk-graph

Housekeeping data for the Harbour hotel as a graph in SQLite: rooms, linen stores and sections in `nodes`,
and the links between them in `edges`. The attendants' tablet app and laundry billing read it.

- `bin/hk <target> "<sql>"` or `bin/hk <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file (see `docs/operations.md`).
- `changes/`: data changes, one `.sql` file each.
- `docs/`: targets and how changes are made, and the linen model.
