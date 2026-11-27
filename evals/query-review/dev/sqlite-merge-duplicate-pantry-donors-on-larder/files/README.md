# pantrygraph

The food bank's donor and stock graph: donors, stock lots, warehouses and partner pantries in `nodes`, and
what links them in `edges`.

- `bin/fb <target> "<sql>"` or `bin/fb <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each, `NNNN_<what>.py`.
- `db/schema.sql`: the schema. `docs/`: the targets, and what the node and edge kinds mean.
