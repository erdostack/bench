# grainbook

Grain contracts between member farms and the co-op's stores, as a graph in SQLite: farms and stores in
`nodes`, memberships and contracts in `edges`. Finance, the disputes desk and the season reports read it.

- `bin/fq <target> "<sql>"` or `bin/fq <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file.
- `changes/`: data changes, one `.sql` file each. See `docs/changes.md`.
- `docs/`: environments, the model, archiving.
