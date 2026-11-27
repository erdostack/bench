# busplan

County home-to-school transport as a graph in SQLite: students, stops, routes, vehicles and schools in
`nodes`, and what links them in `edges`. One database per school year.

- `bin/bp <target> "<sql>"` or `bin/bp <target> --file <file.sql>`: run SQL on a target in `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, `NNNN_<what>.py`.
- `docs/targets.md`: the databases and how data changes are made. `docs/model.md`: the graph.
