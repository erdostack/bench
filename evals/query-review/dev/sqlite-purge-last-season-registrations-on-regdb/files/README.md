# cfa-reg

Player registrations for the county youth football association: players and clubs are nodes, a
`registrations` row is an edge (player registered with club for a season).

- `bin/reg <target> "<sql>"` or `bin/reg <target> --file <file.sql>`: run SQL on a target in `config/targets.toml`.
- `bin/apply <target> <file.sql>`: apply a change file (see `docs/TARGETS.md`).
- `ops/changes/`: data changes, one `.sql` file each, named `YYYY-MM-DD-<slug>.sql`.
- `db/schema.sql`: the schema. `docs/TARGETS.md`: the targets.
