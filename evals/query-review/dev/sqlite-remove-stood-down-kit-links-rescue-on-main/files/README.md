# kitbook

The rescue team's members and kit as a graph in SQLite: members and kit items in `nodes`, who carries what
in `edges`. The callout app and the kit register on the store PC read it.

- `bin/kq <target> "<sql>"` or `bin/kq <target> --file <file.sql>`: run SQL on a target (`config/targets.toml`).
- `bin/apply <target> changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each.
- `docs/targets.md`, `docs/model.md`, `docs/kit.md`.
