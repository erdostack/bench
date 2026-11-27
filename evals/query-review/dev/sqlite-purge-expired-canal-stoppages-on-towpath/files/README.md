# notices-graph

Navigation stoppages on the Wendle & Ouse canals, the structures they close and the notices that announce
them, as a graph in `nodes` and `edges`.

- `bin/tp <target> "<sql>"` or `bin/tp <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes. `db/schema.sql`: the schema. `docs/`: targets, changes, the model.
