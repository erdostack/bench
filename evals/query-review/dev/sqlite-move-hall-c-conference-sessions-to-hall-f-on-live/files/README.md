# venuegraph

The conference centre's bookings as a graph in SQLite: events, their sessions, and the rooms the sessions
are in. The room-booking screen, the signage and the certificate printer read it.

- `bin/vg <target> "<sql>"` or `bin/vg <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a data change (see `docs/changes.md`).
- `changes/`: data changes, one `.sql` file each.
- `db/schema.sql`: the schema. `docs/`: environments, changes, rooms.
