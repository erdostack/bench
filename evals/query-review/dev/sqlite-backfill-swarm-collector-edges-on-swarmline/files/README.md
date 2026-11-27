# swarmgraph

The Calder Moor Beekeepers' Association swarm line, as a graph in SQLite: swarm reports from the public,
the members who collect swarms and the areas they cover, in `nodes`, and what links them in `edges`. The
phone volunteers' app, the swarm map on the website and the collectors' texts use it.

- `bin/sg <target> "<sql>"` or `bin/sg <target> --file <file.sql>`: run SQL on a target from `targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a data change (calls its `run(conn)`).
- `changes/`: data changes, one file each. `tickets/`: copies of the tickets we work from.
- `db/schema.sql`: the schema. `docs/`: targets, changes, the model.
