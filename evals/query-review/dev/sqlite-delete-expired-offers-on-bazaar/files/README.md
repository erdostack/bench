# barterline

Player-to-player trading for Emberfall: players, items, and the edges between them (who owns what,
what is listed for sale, who has made an offer on what).

- `bin/bx <target> "<sql>"` or `bin/bx <target> --file <file.sql>`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each.
- `db/schema.sql`: the schema. `docs/`: targets and the trading model.
