# staffdir

The staff directory: profiles, teams, and who is in which team. One SQLite database (`var/directory.db`,
schema in `db/schema.sql`), written by the nightly sync from the HR system and by team owners in the UI.

- `directory/profiles.py`: profile pages and what a viewer may see.
- `directory/teams.py`: team pages.

Python 3.11+, standard library only.
