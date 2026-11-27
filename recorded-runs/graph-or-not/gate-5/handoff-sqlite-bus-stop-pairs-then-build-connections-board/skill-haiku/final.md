I added `sql/connections.sql`. It takes `:stop_id` and returns `route_id` and `short_name`, one row per route, sorted by `short_name` like `routes_here.sql`. It is plain SQLite with no graph step.

What it does, following the decision record (`no-graph`):

- It takes the stop and its partner across the road. The export records each pair on one stop only, so the partner is found both ways: the stop's own `paired_stop_id`, and any stop whose `paired_stop_id` names it.
- It returns every route that calls at either stop, with school-only routes left out, and `DISTINCT` gives one row per route even when both stops share a route.

I checked it on a small in-memory SQLite dataset (not the real timetable). A pair recorded on one side only shows up from both stops, a route shared by both stops appears once, a school-only route is left out, and a stop with no routes returns no rows.

Not done:

- `boards/board.py` is unchanged. The `TODO` and the empty `connections` list are still there for you to hook in.
- No index was added on `stop.paired_stop_id`. The partner lookup from the other side scans the stop table, which is about 6,900 rows. The record says to add one only if the panel is measured over budget on the real database.
- The query has not been run on the real nightly export. The record's pre-ship trial still applies: about 200 stops, including both sides of several pairs and a school-only stop, checked by hand against the customer services list.
- Open questions from the record still stand: whether a route that only drops passengers at a stop should appear, and whether any pair is recorded twice.

The decision record is unchanged; the decision still stands.
