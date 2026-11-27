# navassets

Structures of the Senn & Ashby Navigation (locks, weirs, bridges, culverts, sluices) and the depots that
maintain them, as a graph in `nodes` and `edges`.

- `bin/nav <target> "<sql>"` or `bin/nav <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file (see `docs/operations.md`).
- `changes/`: data changes, one `.sql` file each. `docs/`: targets, how changes are made, depots, the model.
