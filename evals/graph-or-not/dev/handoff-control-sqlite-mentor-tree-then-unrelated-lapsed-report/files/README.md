# rota

Volunteer rota for the food bank network. Python 3.12, SQLite (`var/rota.db`, backed up nightly, not committed).

- `db/schema.sql` creates the tables.
- Reports are SQL files in `reports/`, run by `python -m rota.report <name> key=value ...`. SQLite only.
