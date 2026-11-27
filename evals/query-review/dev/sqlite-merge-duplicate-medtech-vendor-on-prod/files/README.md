# devicegraph

Medical devices across the trust's three hospitals, with their makers, service contracts and locations,
as a graph in `nodes` and `edges` (SQLite). The maintenance planner and the procurement reports read it.

- `bin/dg <target> "<sql>"` or `bin/dg <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file.
- `changes/`: data changes. `docs/`: environments, model, vendor records.
