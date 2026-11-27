# agendagraph

Events, sessions, rooms and speakers for the conference centre's programme, as a graph in SQLite. The
agenda builder, the speaker portal and the room-booking screens read it.

- `bin/ag <target> "<sql>"` or `bin/ag <target> --file <file.sql>`: run SQL on a target from `targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a data change (calls its `run(conn)`).
- `changes/`: data changes, one file each. `tickets/`: copies of the tickets we work from.
- `db/schema.sql`: the schema. `docs/`: environments, changes, the model and session rules.
