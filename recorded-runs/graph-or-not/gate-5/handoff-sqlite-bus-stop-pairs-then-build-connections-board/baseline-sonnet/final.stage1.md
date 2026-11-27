Decision: no-graph

The Connections panel needs no graph traversal. It is a fixed lookup of the routes at this stop and the routes at its paired stop, which is one hop in each direction. That's a plain SQL query with a join. Kai is right that a bus network is a graph, but this panel doesn't use it as one. You don't need a graph database, an in-memory graph library or recursive SQL, and moving the nightly timetable into a graph database just for this panel would be a lot of machinery for no gain. If a later panel needs real traversal, such as multi-leg journeys, decide then, with that requirement in front of you.

What I added:
- `sql/connections.sql`: a query returning each distinct non-school route (`school_only = 0`) that calls at the screen's stop or at the stop across the road, sorted by `short_name`. The export records each pair on one stop only, so the query looks both ways. It finds the paired stop recorded on this stop and also any stop that records this stop as its pair, and a pair is found from either side.
- `boards/board.py`: `board()` now fills `connections` with the route names from that query, in the same shape as `routes_here`, and the TODO is gone.

Checks, on a small test timetable:
- Both sides of a pair give the same connections, whichever side holds the `paired_stop_id`.
- A school-only route is left out.
- A route calling at both stops appears once.
- A stop with no pair shows only its own routes.
- Speed: on synthetic data of your size (6,900 stops, 380 routes, 41,000 rows), building 1,200 boards took about 0.8 s in total. A minute's refresh of every screen is a small fraction of one core, so it needs no caching. I did not run it against the real export.

Things to know:
- I did not touch `routes_here`, the top line of the board. It still includes school-only routes, since the brief only mentioned the Connections panel. If school routes shouldn't appear there either, that is a one-line change.
- Connections includes the routes at this stop itself, so those also appear in the panel, as you asked ("every route you can catch at this stop or at the stop across the road"). If you'd rather list only the other side's routes, say so.
- The reverse lookup scans `stop.paired_stop_id`, which has no index. At 6,900 stops that doesn't matter. The export is rebuilt every night, so an index would have to be added after each load.
