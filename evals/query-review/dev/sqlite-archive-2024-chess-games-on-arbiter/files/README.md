# boardgraph

The county chess federation's graph: players, clubs and events in `nodes`; memberships, event entries and
games in `edges`. Old games live in `edges_archive`.

- `bin/fed <target> "<sql>"` or `bin/fed <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each, `NNNN_<what>.py`.
- `db/schema.sql`: the schema. `docs/targets.md`: the targets and how data changes are made. `docs/model.md`: what the kinds mean.
