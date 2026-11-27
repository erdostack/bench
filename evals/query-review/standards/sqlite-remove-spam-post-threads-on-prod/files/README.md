# cobblewick-forum

The data behind the Cobblewick community site, in SQLite: people and who knows whom, forums with their
members and moderators, posts and the comment threads under them, likes and tags.

- `bin/tq <target> "<sql>"`: run SQL on a target in `config/targets.toml`.
- `bin/apply <target> changes/<file>.sql`: apply a change file (see `docs/changes.md`).
- `scripts/reset_scratch.py`: rebuild `data/scratch.db` from prod.
- `db/schema.sql`; `docs/changes.md`, `docs/model.md`, `docs/moderation.md`.
