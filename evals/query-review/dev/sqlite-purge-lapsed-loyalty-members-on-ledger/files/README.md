# pointsgraph

The loyalty programme as a graph: members, stores and rewards in `nodes`, and what links them in `edges`.

- `bin/pg <target> "<sql>"` or `bin/pg <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each, `NNNN_<what>.py`.
- `db/schema.sql`: the schema. `docs/`: the targets, and what the node and edge kinds mean.
