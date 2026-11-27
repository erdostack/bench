# stop-boards

Server for the screens at bus stops. Each night the scheduling system writes the timetable to
`var/timetable.db` (SQLite, not committed; tables in `db/schema.sql`) and the board server reads it.

- `boards/board.py` builds what one screen shows.
- Queries live in `sql/`, one file per query, named parameters.
- Python 3.12, standard library only.

## Decision: the Connections panel (2026-11-24)

Decision: recursive-sql (read: stay on the SQLite export; no graph database)

Customer services: a stop's Connections are the routes at that stop or at the stop across the road, never the
school-only routes. 6,900 stops, 380 routes, 41,000 stop-route rows, nightly; 1,200 screens once a minute. Kai's
graph database was rejected: one lookup on a nightly file.
