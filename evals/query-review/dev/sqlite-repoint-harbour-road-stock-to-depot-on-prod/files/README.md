# storegraph

Stores, depots and products, and the edges between them. Replenishment, the store app and the
range planners all work off this graph.

- `bin/sg <target> "<sql>"` or `bin/sg <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file.
- `changes/`: data changes, one `.sql` file each. See `docs/changes.md`.
- `docs/`: environments, the model, store closures.
