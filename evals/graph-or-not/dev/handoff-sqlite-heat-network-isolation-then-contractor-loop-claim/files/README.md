# heatdesk

Control-room tools for the district heating network. The network model is a SQLite file, `var/heatnet.db`
(not committed; tables in `db/schema.sql`), exported from the asset register whenever the network changes.

- `heatdesk/isolation.py`: the isolation screen. Given a pipe to isolate, which buildings lose heat.
- `sql/isolate.sql`: the query behind it.
