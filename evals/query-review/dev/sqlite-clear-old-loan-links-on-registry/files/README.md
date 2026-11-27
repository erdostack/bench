# collectiongraph

The museum's collection graph: objects, venues (our galleries, stores and the institutions we lend to),
and typed links between them.

- `bin/cg <target> "<sql>"` or `bin/cg <target> --file <file.sql>`: run SQL on a target from
  `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each, `NNNN_<what>.py`.
- `db/schema.sql`: the schema.
- `docs/`: how the targets are used, and what the link kinds mean.
