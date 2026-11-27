I wrote `sql/nearby_segments.sql`. It takes `:segment_id` and `:hops` and returns one `segment_id` per row for every segment within `:hops` neighbour-steps. The starting segment is not included, and `:hops = 0` returns nothing.

Two segments count as neighbours when they share a junction (`j1` or `j2`). The walk is a recursive query over `segment`, and it uses the existing `segment_j1` and `segment_j2` indexes.

The network has loops, so a segment can be reached by many routes. The query keeps one row per segment and depth and stops at `:hops`, so loops can't make the walk grow with the number of routes. A final `SELECT DISTINCT` leaves one row per segment.

I tested it on a small made-up network. It had a four-segment loop, a spur and a self-loop segment, and I tried `:hops` from 0 to 4. The results were correct each time. I couldn't run it against `var/streets.db`, because that file isn't in the repo, so I have no timing on the real network.

I didn't change anything else. I kept to the recursive SQL on SQLite that `docs/graph/DECISION.md` records. The record suggests adding an index on `segment_route(segment_id)` for the operator lookup. That isn't part of this query, so I left it alone.
