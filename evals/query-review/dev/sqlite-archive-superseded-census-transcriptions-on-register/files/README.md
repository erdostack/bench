# parishgraph

The family-history society's transcription archive: people, the census and parish records they appear
in, and the register volumes those records come from, as `entity` and `relation` rows in SQLite.
Volunteers transcribe through the volunteer site; members search it.

- `bin/reg register "<sql>"` or `bin/reg register --file <file.sql>`: run SQL on the register.
- `bin/apply register changes/<file>.py`: apply a change file (calls its `run(conn)`).
- `changes/`: data changes, one file each. `db/schema.sql`: the schema.
- `docs/register.md`: the database and how it is changed. `docs/model.md`: what the rows mean.
