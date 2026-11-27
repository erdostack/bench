# bylaw-register

The clerk's office tools for the municipal bylaw register. `var/register.db` is a SQLite copy of the
register, refreshed every night from the records system (not committed; tables in `db/schema.sql`).

- `python -m bylaws.web` runs the internal site (search, bylaw pages, repeal impact).
- Python 3.12.
