# wyvern-donor-ops

Donors, donor centres and donations of the Wyvern Blood Service, stored as a graph in `nodes` and
`edges` (SQLite).

- `bin/ws <target> "<sql>"` or `bin/ws <target> --file <file.sql>`: run SQL on a target from
  `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes. `db/schema.sql`: the schema. `docs/`: targets, the model, how changes are made.
