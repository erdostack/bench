# permits

The planning department's permit application tracker.

- Python 3.11, Flask, Postgres 15 with PostGIS (shared with the GIS team's nightly jobs).
- `db/schema.sql` holds the tables this app reads. `parcel_adjacency` is written by the GIS team's nightly job
  from the parcel geometries; this app only reads it.
- Batch jobs (weekly letters, monthly statistics) run from cron on the app server.
