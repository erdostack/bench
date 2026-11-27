# kinfolk

The society's family-history graph: people, places, and the events (birth, baptism, burial) that join a
person to a place. SQLite, `nodes` and `edges`. The public search and members' family trees read it.

- `bin/fq <server> "<sql>"` or `bin/fq <server> --file <file.sql>`: run SQL on a server from `config/servers.toml`.
- `bin/apply <server> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes. `tickets/`: copies of the tickets we work from.
- `docs/servers.md`: the servers and how changes reach live. `docs/places.md`: how places work.
