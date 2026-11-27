Transit DB roast: the stop page is wrong, not just slow

The worst problem is in the stop page query. routes_at_stop.sql matches the comma-separated stop_sequence with LIKE '%' || :stop_id || '%', so it is a substring search, not a membership test. Stop 1 lists all 310 routes, because every route's stop list contains a digit 1. The real answer is 2 routes (145 and 270). Across the copy, 999 of the 4,800 stop pages list at least one route that does not call there. The fix is a route_stop table with one row per route and stop, an index, and an indexed join. The planner's search is built on the same LIKE lookup, so it inherits the problem.

Ranked list (full detail in findings.json):

1. routes_at_stop.sql (critical): substring matching gives phantom routes on 999 stop pages and scans the whole route table on each request. Replace it with an indexed route_stop table.
2. stop_sequence (high): a packed comma list with no foreign key to stop, and foreign keys are off in the copy (foreign_keys = 0). Nothing can index it, join it or check it. Move the order into route_stop with a seq column and a real foreign key.
3. one_change (medium): stops_of is run again for every candidate route, and the candidate list is inflated by the LIKE false positives. The planner also never checks for a direct route. At this size it is fast (200 random pairs in 0.19 s), so this is about structure, not current speed.
4. stops_of (low): unpacks fetchone() without checking for None, so a missing route raises TypeError.
5. headway (low): minutes has no positive check, and the foreign key is not enforced in the copy.
6. stop (low): no range checks on lat and lon. 478 stops (about 10%) are served by no route. That might be intended, but the schema cannot tell closed stops from a gap in the nightly rebuild.
7. routes_at_stop.sql (low): the ORDER BY short_name sort puts T11 before T2.

Limits: I worked from the files and read-only queries against the copy in transit.db. I did not measure production-scale timings, and the copy has 310 routes, so the performance points are about structure, not what users feel today.
