# tipnet

Tipping-bucket rain gauges across the county network, stored as a graph in SQLite: stations, the gauges
installed at them, and every reading (one bucket tip, 0.2 mm) in `nodes`, with the links between them in
`edges`.

- `bin/obsq <target> "<sql>"` or `bin/obsq <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each.
- `db/schema.sql`: the schema. `docs/`: targets, and how readings are quality-controlled.
