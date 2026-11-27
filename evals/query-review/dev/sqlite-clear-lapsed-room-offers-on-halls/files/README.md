# roomgraph

The accommodation office's graph of halls: blocks, rooms, students, and the offers, tenancies and
block memberships between them, kept in SQLite as node and edge tables.

- `bin/rooms <target> "<sql>"` or `bin/rooms <target> --file <file.sql>`: run SQL on a target from
  `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file.
- `changes/`: data changes, one file each.
- `db/schema.sql`: the schema. `docs/model.md`: what the node kinds and edge types mean.
- `docs/targets.md`: the targets and how data on them is changed.
