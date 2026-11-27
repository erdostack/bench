I rewrote `trapped_junctions(conn)` in `oneway/trapped.py` as one recursive SQL query, as `docs/graph/DECISION.md` says (recursive-sql). The signature is unchanged, so `oneway/report.py` needs no edit. It returns the sorted ids of the junctions the draft traps.

What changed in the rule:
- A junction is trapped if the ring road cannot reach it, or it cannot reach the ring road, following road segments under the draft's directions. The old check only tested the second direction.
- Footpath segments are not used as roads.
- Junctions with no road segment at all are not reported. This covers the footpath-only junctions you specified. I also left out junctions with no segments of any kind, which the rule does not mention; tell me if the traffic team wants those reported.
- The 25-step cap is gone, so a long one-way loop is no longer reported as trapped just because it is long.

Checks I ran:
- On five synthetic drafts of 1,450 junctions and 1,900 segments, the query matched a plain Python reference that searches both directions with no cap. Each query took about 120 to 150 ms, with no indexes.
- A small hand-made draft gave the expected result, and `python -m oneway.report` ran on a tiny file.

Not done, and needs your call:
- The decision file's 10 ms figure assumes indexes on `segment(a)` and `segment(b)`. I did not add them, because that means writing to each planner's draft file or changing the exporter's schema. Adding them in the exporter would bring the time down.
- The real draft was not in the repo, so I have not run the check on last week's draft. The decision lists that as the trial to pass before the fix is accepted. Compare its output with the 63 junctions flagged last week, and expect the count to change. The market loop should drop out of the report.
- The synthetic drafts flag 660 to 770 junctions each, far more than the real draft's 63, so those timings show the cost of the work and say nothing about the real flag count.

The only file changed in the repo is `oneway/trapped.py`.
