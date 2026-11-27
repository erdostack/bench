# washorders

Spinwell Laundrettes' service-wash orders as a graph in SQLite: orders, customers, shops and machines in
`nodes`, and what links them in `edges`. The counter tablets, the collection texts and the weekly takings
report use it.

- `bin/wo <target> "<sql>"` or `bin/wo <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a data change.
- `changes/`: data changes, one file each. `db/schema.sql`: the schema.
- `docs/targets.md`, `docs/model.md`, `docs/retention.md`.
