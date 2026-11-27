I added `sql/connections.sql` in the stop-boards repo. It takes `:stop_id` and returns `route_id` and `short_name`, one row per route, ordered by `short_name` like `routes_here.sql`. It is plain SQLite and I did not touch `boards/board.py`, so the hook-in is still yours.

What it returns: the routes that call at the stop on the other side of the road. The schema says the pair is recorded only once, on one of the two stops, so the query finds the partner in both directions. I checked it on a small in-memory copy of `db/schema.sql` with pairs recorded on either side, a stop with no partner, and duplicate-free output. All five cases returned the expected routes.

Two things to confirm, because the decision itself is not in the repo:
- I read "Connections" as the partner side's routes. If the panel should be something else, such as routes that call at both stops, or should leave out routes already in `routes_here`, the query needs changing.
- A route that also calls at this stop still appears, because the query does not exclude it.
