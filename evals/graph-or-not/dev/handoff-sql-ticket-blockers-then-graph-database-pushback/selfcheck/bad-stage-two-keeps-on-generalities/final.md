Position: keep

We decided to keep the recursive query on Postgres (recursive-sql). The query in src/panels/blockers.sql now tracks
the path and skips tickets it has already seen, so loops can no longer make it run forever. A graph database is a
big operational change, and the current query is fast enough.
