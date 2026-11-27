`sql/connections.sql` is in place and takes `:stop_id`. It returns `route_id` and `short_name`, one row per route, in SQLite like `sql/routes_here.sql`. The file was already in the repo when I started, so I checked it and left it unchanged.

What it returns: every route that calls at this stop or at the stop across the road, sorted by `short_name`, with school-only routes (`school_only = 1`) left out. A route that calls at both stops appears once.

The export records each pair on one stop only. So the query finds the paired stop in both directions: the `paired_stop_id` held by this stop, and any stop that holds this stop as its `paired_stop_id`. A screen on either side of the road gets the same panel.

I ran it on a small in-memory database built from `db/schema.sql`:
- Both sides of a pair gave the same result.
- The school-only route was excluded.
- A route calling at both stops was listed once.
- An unpaired stop showed only its own routes.
I did not run it against the real nightly export.

Things to know:
- `boards/board.py` already calls this query and fills `connections` from it, in the same shape as `routes_here`. You said you'd hook it in yourself, so you may want to check that wiring matches what you intended. I didn't touch it.
- The panel includes the routes at this stop itself, as well as the other side's. That follows "every route you can catch at this stop or at the stop across the road".
- `routes_here` still includes school-only routes. I left it alone because you only asked about the Connections panel.
- The reverse lookup scans `stop.paired_stop_id`, which has no index. At about 6,900 stops that doesn't matter.
