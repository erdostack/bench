`sql/connections.sql` is written. It takes `:stop_id` and returns `route_id` and `short_name`, one row per route, ordered by `short_name`.

It follows the recorded decision in `docs/graph/DECISION.md` (no graph, one join). It collects the routes that call at the stop itself or at the stop across the road, and leaves out school-only routes (`school_only = 0`). Each route comes back once, because it filters `route` with `IN (...)` and nothing is joined per route.

The export records each pair on only one of the two stops. So the query finds the paired stop in both directions: through this stop's own `paired_stop_id`, and through any stop whose `paired_stop_id` is this stop. If you read only the first, half the stops would miss their opposite-side routes.

I checked it on a small in-memory SQLite database built from `db/schema.sql`. A stop and its pair returned the same list, the school-only route was dropped, a route serving both sides of the road appeared once, and a stop with no pair returned only its own routes. I did not run it against real data.

Reading the pairing backwards scans `stop` at the moment, because nothing indexes `paired_stop_id`. The decision record measured that as fine (12 ms worst case at 20 screens a second on synthetic data of the stated size). It also says an index on `stop(paired_stop_id)` is the ordinary fix if it ever shows up, and that this is for the data team to decide. I did not add one.

I did not touch `boards/board.py`, since you said you'd hook it in. The query reads `:stop_id` as a named parameter, so the call is `conn.execute(query("connections"), {"stop_id": stop_id}).fetchall()`. The TODO there can then be replaced by that result, as with `routes_here`.
