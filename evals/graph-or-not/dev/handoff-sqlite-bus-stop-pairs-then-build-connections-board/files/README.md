# stop-boards

Server for the screens at bus stops. Each night the scheduling system writes the timetable to
`var/timetable.db` (SQLite, not committed; tables in `db/schema.sql`) and the board server reads it.

- `boards/board.py` builds what one screen shows.
- Queries live in `sql/`, one file per query, named parameters.
- Python 3.12, standard library only.
