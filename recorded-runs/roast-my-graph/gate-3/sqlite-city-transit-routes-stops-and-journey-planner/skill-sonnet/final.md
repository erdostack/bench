Yes, something is badly wrong: the stop page shows routes that do not call at the stop.

`db/routes_at_stop.sql` matches the stop id as a substring of `route.stop_sequence`, a comma-separated string. I ran it read-only on `transit.db` (SQLite 3.53.1). 999 of the 4,800 stops return wrong routes, 35,245 extra rows in all. Stop 7 returns 309 of 310 routes, and only one calls there. `stop_page` passes that result straight to the user.

Findings (also in `findings.json`, full write-up in `docs/graph/ROAST.md`):

1. `routes_at_stop.sql` (critical): the substring match above. After the fix below it becomes a join on `route_stop`, which returns 1 route for stop 7.
2. `stop_sequence` (critical): the stored element behind it. Replace it with a `route_stop (route_id, seq, stop_id)` table, with an index on `(stop_id, route_id)`. The migration splits the strings with a recursive query (11,187 rows on your copy, matching the ids in the strings), then drops the column. Your nightly rebuild has to write `route_stop` too.
3. `one_change` (low): the planner's results are correct, because it re-checks every route the SQL returns. It does extra work for the false candidates, but it took 3 to 16 ms per query in my in-memory tests. A single join over `route_stop` replaces it; I checked it against 3 pairs.

Holds up: `headway`, `route.short_name` and `mode`, and the `stop` key.

Not checked: the nightly rebuild is not in the repo, so reconcile the migration with it. Request rates and latency targets are not stated.
