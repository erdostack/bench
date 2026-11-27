# fenwick-carclub

The Fenwick Car Club's fleet as a graph in SQLite: cars, the zones they live in and the depots that clean
and service them. The members' booking app and the depot crews' job lists read it.

- `bin/cc <target> "<sql>"` or `bin/cc <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a data change (see `docs/targets.md`).
- `changes/`: data changes, one `.sql` file each. `db/schema.sql`: the schema. `docs/`: targets and the model.
