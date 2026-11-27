# marchesflow

Consignment planning for Marches Freight's regional rail services: customers, consignments, trains and
terminals as a graph in `nodes` and `edges` (SQLite).

- `bin/fq <target> "<sql>"` or `bin/fq <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> migrations/data/<file>.py`: apply a data migration (calls its `run(conn)`).
- `migrations/data/`: data migrations.
- `db/schema.sql`: the schema. `docs/`: environments, the model, terminal changes.
