# commons

The neighbourhood community platform: member profiles, follows, groups and events.

- Python 3.12, Starlette, SQLite in WAL mode on the app server (`var/commons.db`, replicated with Litestream; not
  committed). Tables in `db/schema.sql`.
- Profile page data is assembled in `commons/profile.py`.
