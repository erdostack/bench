# hartwell-loans

The loans ledger of the Hartwell Tool Library: members, tools and the loans and reservations between them,
kept as a node table and an edge table in SQLite. The volunteers' desk app and the website's "my loans" page
read and write it.

- `bin/ledger <target> "<sql>"`: run SQL on a target from `config/targets.toml`.
- `bin/apply <target> changes/<file>.py`: apply a data change (calls its `run(conn)`).
- `scripts/refresh_practice.py`: copy `shed` to `practice`.
- `docs/targets.md`: the targets and how data changes are made. `docs/model.md`, `docs/archive.md`.
