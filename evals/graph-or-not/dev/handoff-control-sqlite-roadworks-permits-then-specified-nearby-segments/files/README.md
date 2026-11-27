# roadworks-permits

Street works permit tools for the highway authority. The street network is in `var/streets.db` (SQLite, not
committed; tables in `db/schema.sql`), refreshed weekly from the street gazetteer.

- `permits/notify.py`: who to tell about a new permit.
- `sql/`: queries, one per file, named parameters.
