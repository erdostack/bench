# objectgraph

The museum's collection as a graph: objects, the collections they belong to and the places they are, in
`nodes` and `edges`. The collections website, the loans desk and the registrar's annual return read it.

- `bin/og <target> "<sql>"` or `bin/og <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file.
- `changes/`: data changes, one `.sql` file each. See `docs/changes.md`.
- `docs/`: environments, the model, deaccessioning.
