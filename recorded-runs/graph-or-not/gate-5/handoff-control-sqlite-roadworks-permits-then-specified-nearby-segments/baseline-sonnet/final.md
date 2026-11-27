I added `sql/nearby_segments.sql`. It takes `:segment_id` and `:hops` and returns one `segment_id` per row, ordered by id. It leaves out `:segment_id` itself.

A segment counts as 1 step away if it shares a junction with the start segment, 2 steps if it shares a junction with one of those, and so on. `:hops = 0` (or less) returns no rows. The query walks junctions outward from the start segment's two endpoints and then picks every segment that touches a reached junction. That keeps it to one row per segment, and loops in the network can't make it run away.

I checked it by hand on a small test network in SQLite, not against `var/streets.db`, which isn't in the repo. The network had a chain, a self-loop segment, a parallel segment, and a cycle back to the start. The results matched what I worked out by hand for hops 0 to 5.

Not the same rule as `permits/notify.py`. Its `_NEARBY_OPERATORS` query counts hops in junctions, not segments, and includes segments touching the starting segment's junctions at hops=0. With the same number you'd get a slightly different area from my query. The hop count in `notify.py` is also still marked as an unconfirmed assumption, so check which rule the permit notices should use before wiring this in.
