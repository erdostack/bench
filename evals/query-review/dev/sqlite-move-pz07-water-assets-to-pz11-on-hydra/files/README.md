# assetreg

The water network asset register: pressure zones, hydrants, valves and mains, and the edges between them,
in SQLite (`db/schema.sql`, `docs/zones.md`).

- `bin/hx <target> "<sql>"` or `bin/hx <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes. `docs/targets.md`: the targets and how changes are made.
