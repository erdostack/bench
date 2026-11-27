# skyfare search

Flight search for the booking site. The timetable is a SQLite file built nightly from the schedule feed
(`db/schema.sql`); the search API reads it read-only.

- `search/itineraries.py`: builds itineraries from queries in `sql/`.
- `sql/`: SQLite queries with named parameters.
