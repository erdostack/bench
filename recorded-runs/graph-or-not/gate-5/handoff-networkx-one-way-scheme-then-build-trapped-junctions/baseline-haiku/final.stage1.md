Decision: in-process-library

This is a graph problem, but a small one. A draft is about 1,450 junctions and 1,900 segments, and the check is reachability in a directed graph with no depth limit. The fix is to load the draft's road segments into memory and run two breadth-first searches from the ring road: one forward over the directed road edges and one backward over reversed edges. Each junction is then reported as trapped if it is missing from either set. Both searches are linear in the size of the draft and run in well under a second on a laptop. networkx is already installed on the planners' machines, so `ancestors` and `descendants` from networkx can do the same job if you want a library, though the standard library is enough.

A graph database does not fit: each draft is a single file used by one laptop, and standing up a database server for it adds a service to run without any gain. recursive-sql would also work on the draft file, but cycles in a directed road network need a UNION-based walk, and the in-memory version is simpler to get right and to test.

What is wrong with the current check (oneway/trapped.py), tested on a synthetic draft loaded into an in-memory copy of db/schema.sql:
- The 25-step cap is the reason for the 63-junction report, but it is not the only error. It cuts off the search, so junctions 1 to 5 of a 30-step one-way run are reported trapped even though they can reach the ring, while junction 6 and beyond on that run are not reported at all.
- The check looks only forward. It never asks whether the ring road can be driven to the junction. A junction with a one-way segment out to the ring and nothing coming in (junction 34 in my test) is not reported, but the traffic team's rule reports it.
- `_moves` ignores `mode`, so footpath segments are treated as drivable. A junction connected to the ring only by a footpath is treated as reachable. Under the rule it should not be reported as trapped, and that needs the `mode = 'road'` filter on both directions.

Rule for the replacement, as written by the traffic team: a junction is trapped if it cannot be driven to the ring road or cannot be driven to from the ring road, using road segments and the draft's directions only. A junction that is only on footpaths is not reported.

Points for the traffic team to confirm before the code is changed:
- A junction with no segments at all (isolated in the draft) is not on footpaths, so the footpath exclusion does not cover it. Under the literal rule it is trapped. My synthetic test flagged such junctions and the current code reports them. Please say whether these are reported.
- The ring-road junctions themselves (`on_ring = 1`) are the targets and should not be reported.

The reverse check will add junctions to the report, not remove them. Expect the count to change in both directions when the draft is re-run, and compare against a hand-checked sample before the planners rely on it.
