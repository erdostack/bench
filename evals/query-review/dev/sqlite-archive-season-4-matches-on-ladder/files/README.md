# ladderline

The ranked ladder of the Emberfall arena: teams, players, and the matches between teams, stored as a
graph in `nodes` and `edges`. Finished seasons are moved to `edges_archive`.

- `bin/lad "<sql>"` (or `bin/lad --file <file.sql>`): run SQL on the ladder database.
- `bin/apply migrations/data/<file>.py`: apply a data migration (calls its `run(conn)`).
- `migrations/data/`: data migrations. `db/schema.sql`: the schema. `docs/`: how the database is run.
