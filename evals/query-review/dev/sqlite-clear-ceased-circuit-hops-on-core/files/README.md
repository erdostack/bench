# fibremap

Inventory of the metro fibre network: ports on patch panels and splice trays, the circuits sold over them,
and one `hops` row per pair of consecutive ports a circuit passes through (the path tracer draws these).

- `bin/fm <target> "<sql>"` or `bin/fm <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each, `NNNN_<what>.py`.
- `db/schema.sql`: the schema.
- `docs/TARGETS.md`: what each target is.
