# Graph decision

Decision: recursive-sql

The trapped-junctions check is a reachability question on one draft's directed road network, with no fixed depth, and it fits the SQLite draft file the planners already open: two recursive queries (from the ring road forward and backward) and a set difference answer it in about 10 ms per draft with indexes on the segment endpoints, and the current script's bugs (a 25-step cap, footpaths counted as roads, one direction only) are fixed inside that query rather than by a new store. The finding it turns on is the size of the graph: 1,450 junctions and 1,900 segments, which a database handles without a graph engine.

## Workload facts

- Junctions per draft: about 1,450 (stated by the user)
- Segments per draft: about 1,900 (stated by the user); about 1,450 junctions with 1,900 segments is an average of 2.6 segments per junction, counting both ends (derived: 2 x 1,900 / 1,450 = 2.62)
- Drafts run: two planners, 20 or 30 drafts a week each, so 40 to 60 drafts a week in total (stated by the user; 2 x 20 = 40, 2 x 30 = 60)
- Last week's draft: 63 junctions flagged, most on the long one-way loop through the market streets (stated by the user)
- Trapped rule, as the traffic team states it: a junction is trapped if the drive from it to the ring road cannot be made, or the drive from the ring road to it cannot be made, under the draft's directions; footpaths are not roads; a junction that is only on footpaths is not reported (stated by the user)
- Ring: junctions with `on_ring = 1` are the ring road, two-way all round (`db/schema.sql`)
- Directions: `oneway` 0 is two-way, 1 is only a to b, -1 is only b to a; `mode` is `road` or `foot` (`db/schema.sql`)
- Existing check: `MAX_STEPS = 25` stops each search after 25 steps, so a long one-way loop reads as trapped (`oneway/trapped.py`, line 4 and the loop at lines 26 to 34)
- Existing check ignores `mode`: `_moves` builds moves from every segment, footpaths included (`oneway/trapped.py`, lines 7 to 14)
- Existing check tests one direction only: it asks whether the ring road can be reached from each junction, not whether the junction can be reached from the ring road (`oneway/trapped.py`, lines 17 to 36)
- Existing check does not exclude junctions that have only footpath segments (`oneway/trapped.py`, line 22)
- Schema has no index on `segment(a)` or `segment(b)` (`db/schema.sql`); measured below, the indexes take the recursive query from about 205 to 258 ms to about 9 to 10 ms per draft
- Measured, synthetic (three seeds, generator in scratch, not a real draft: 1,450 junctions, 1,900 segments, about 20% footpath segments, 60 ring junctions): existing script 276 to 457 ms per draft and flagged 1,100 to 1,351 junctions; plain Python reference for both directions 3 to 12 ms; recursive SQL for both directions 205 to 258 ms without indexes, 9 to 10 ms with indexes on `a` and `b`; recursive SQL and the reference agreed on all three drafts (measured, sqlite 3.53.1, Python 3.13 on this machine, not the planners' Python 3.12)
- Caveat on the synthetic drafts: they flag 1,100 to 1,350 junctions each, far more than the 63 in the real draft, so they are much more fragmented than the real network; the timings show the cost of the work at this size, not the real flag count
- Derived: 40 to 60 drafts a week x about 10 ms per draft with the indexes = under 1 second of database time per week across both planners (derived from the measurement above)
- unknown: the real draft files and their exact contents; why the existing script flags 63 and how many of those are the market loop alone (needs a run on last week's file, which is not in the repo); whether the traffic team counts a ring junction with no road segment as on the ring; the planners' latency expectation for the check (not stated); whether all planners' laptops run SQLite 3.8.3 or later for recursive queries (not checked on their machines)

## Options considered

- graph-database (a dedicated graph store, the transport modelling consultant's proposal): rejected, because the graph is 1,450 junctions and 1,900 segments, a size a SQLite file handles in about 10 ms per draft with indexes, and a second store would have to be installed on two planners' laptops and kept in step with the sketch tool's export
- in-process-library (the segments loaded into memory with networkx, which the planners' machines already have): passed over, because recursive-sql holds at the rung before it; this option would also meet the need, since the plain Python reference runs in 3 to 12 ms, and it is the fallback if the recursive query proves hard to keep correct
- recursive-sql (recursive queries on the draft file, which is already SQLite): chosen, because the check is reachability from the ring road in each direction to a data-dependent depth, the draft file is already the planners' store, and the measured cost is about 10 ms per draft with the two indexes on `a` and `b`
- no-graph (plain joins, no traversal): rejected, because the rule asks whether a junction can be reached and can reach the ring road by following one-way segments to any depth, which is a traversal and not a join across a link table once

## What would change the decision

- A draft several times larger than this one, or many drafts checked at once for a city-wide scheme, measured over the time the planners accept on their laptops, would move this to in-process-library (the time budget is set by the planners, not the repo)
- A question about routes between pairs of junctions (shortest paths, every route between two points) rather than reachability of the ring road would move this to in-process-library or, if the data grows, to graph-database
- A need to re-run the check on every edit of the sketch tool in real time, with a measured latency over the planners' budget, would move this to in-process-library, with a reload on each edit
- Trial before the fix is accepted: run the corrected check on last week's real draft, compare it with the 63 flagged junctions one by one, and confirm that the market loop is no longer reported and that no footpath-only junction is reported
