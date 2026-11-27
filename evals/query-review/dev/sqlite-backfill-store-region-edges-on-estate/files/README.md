# estate

The store estate as a graph: stores and regions in `nodes`, and `edges` between them.

- `bin/est <target> "<sql>"` or `bin/est <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file (see `docs/operations.md`).
- `changes/`: data changes, one `.sql` file each.
- `docs/`: the targets and how changes are made, and the model.
