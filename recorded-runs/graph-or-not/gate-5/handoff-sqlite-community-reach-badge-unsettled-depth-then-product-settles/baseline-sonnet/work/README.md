# commons

The neighbourhood community platform: member profiles, follows, groups and events.

- Python 3.12, Starlette, SQLite in WAL mode on the app server (`var/commons.db`, replicated with Litestream; not
  committed). Tables in `db/schema.sql`.
- Profile page data is assembled in `commons/profile.py`.

## Decisions

- **"N introductions away" badge** (`commons/profile.py`, `sql/introductions.sql`): the badge only ever shows 1
  ("follows you") or 2 ("friend of a friend"), as settled by growth and product. It is plain indexed SQL lookups in
  SQLite, with no recursion and no graph database or graph library. Measured 9 ms p95 for the two-step lookup on a
  copy of the database, against the 150 ms budget at a peak of 70 profile views a second. Neo4j was considered
  and rejected: a second database to run, sync and secure for one badge. Revisit only if the badge is
  extended past 2 steps, and then measure a bounded search on a copy of the real database first.
