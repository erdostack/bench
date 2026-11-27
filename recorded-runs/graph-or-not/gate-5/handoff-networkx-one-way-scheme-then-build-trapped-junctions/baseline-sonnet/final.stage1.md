Decision: in-process-library

Keep this a small Python script and use networkx, which is already on the planners' machines. This is a real graph problem: reachability to and from the ring road on a directed graph. But a draft of 1,450 junctions and 1,900 segments is tiny, and the planners run it on laptops against a SQLite file, so a graph database would add a server and an import step for nothing. Recursive SQL could do it, but "can reach the ring" and "can be reached from the ring" are awkward there, and loop-safe recursive CTEs are easy to get wrong.

Why the check was wrong, and what I changed (`oneway/trapped.py`):
- The 25-step cap is why the market-street loop was flagged. A one-way loop longer than 25 junctions never reaches the ring within the cap. There is no cap now.
- The check only looked one way. It asked whether you can drive from the junction to the ring, and never whether you can drive from the ring to it. Both directions are checked now. A junction is trapped if either fails, so one-way sinks and unreachable sources are both reported.
- The old code built moves from every segment, so footpaths counted as roads. Only `mode = 'road'` segments count now, and a junction that is only on footpaths is not reported.
- The ring is collapsed into one virtual node, so two reachability sweeps (`ancestors` and `descendants`) answer it for every junction at once. Before, it ran a separate search from each junction.

Checks on a small hand-built draft:
- A 60-junction one-way loop through the ring is not flagged.
- A junction you can enter but not leave is flagged, and so is one you can leave but not enter.
- A junction reached only by a footpath is not flagged, and neither is a junction with no segments at all.
- I did not have a real draft file, so I have not rerun your 63-junction draft. Expect the count to drop to the junctions that are really trapped. Run `python -m oneway.report var/<draft>.db` on it and compare.

Behaviours to be aware of:
- Junctions with no road segments are not reported, whether they have footpaths only or nothing at all.
- If a draft has no ring junction on any road, every road junction is reported, since none can reach the ring.
- `oneway.report` is unchanged.
