# meadowbank-register

Share register for Meadowbank Community Energy: members, the sites they own shares in, the share offers
they pledged to, and the edges between them.

- `bin/mq <target> "<sql>"` or `bin/mq <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each.
- `db/schema.sql`: the schema. `docs/`: targets and the register model.
