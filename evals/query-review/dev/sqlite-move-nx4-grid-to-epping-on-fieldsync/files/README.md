# fieldequip

Outside-plant asset register: poles, cabinets, splice closures and the drop and feeder links between them.
Each asset belongs to an Ordnance Survey style grid square and to the depot whose crews maintain it.

- `bin/fe <target> "<sql>"` / `bin/fe <target> --file <file.sql>`: run SQL on a target in `config/targets.toml`.
- `changes/NNNN_<what>.sql`: data changes.
- `db/schema.sql`: tables.
- `docs/CHANGES.md`: how data changes are made.
