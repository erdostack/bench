# pedalnet

The city bike-share scheme as a graph in SQLite: docking stations and bikes in `nodes`, and in `edges`
where each bike is docked and where the dock readers have seen it.

- `bin/pn <target> "<sql>"` or `bin/pn <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a data change (see `docs/targets.md`).
- `changes/`: data changes, one `.sql` file each.
- `queries/`: the saved queries the rebalancing planner runs.
- `db/schema.sql`: the schema. `docs/`: targets and the model.
