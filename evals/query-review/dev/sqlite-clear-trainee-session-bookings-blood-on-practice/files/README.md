# marsh-sessions

Donation sessions and bookings of the Marsh Blood Service call centre, as a graph in `nodes` and `edges`
(SQLite).

- `bin/ms <target> "<sql>"` or `bin/ms <target> --file <file.sql>`: run SQL on a target from
  `config/targets.toml`.
- `scripts/build_practice.py`: throw the practice copy away and build a fresh one.
- `db/schema.sql`, `docs/targets.md`, `docs/model.md`.
