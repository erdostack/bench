Decision: in-process-library

Use a graph library in the script. You don't need a graph database or recursive SQL. This is a whole-graph reachability pass over a snapshot file, run as a batch on a laptop. networkx is already installed on the planners' machines.

Why the check is wrong today, and it isn't the data store. oneway/trapped.py differs from the traffic team's rule in three ways:
- It stops after 25 steps (MAX_STEPS). That is where most of your 63 flags come from, since the market loop is longer than that.
- It only checks whether you can get from a junction to the ring, never from the ring to the junction.
- It ignores the segment mode, so footpaths are treated as roads, and junctions that are only on footpaths aren't excluded.

How to fix it (I did not change any code): build a directed graph from road segments only (oneway 0 gives two edges, 1 gives a to b, -1 gives b to a). Work out what is reachable from the ring and what can reach the ring, once each, with no step cap. A road junction is trapped if it is missing from either set. Junctions that touch no road segment are not reported.

The numbers it turns on:
- Size: about 1,450 junctions and 1,900 segments, so up to about 3,800 directed moves per draft. That is tiny.
- Measured: on a synthetic draft of that size (random data, not your real drafts), the networkx version took 0.86 s and 1.5 MB. 30 drafts a week is about 27 s of work a week, so there is nothing for a server to serve.

Not found: your real drafts (none in the repo), so I can't say how many junctions are footpath-only or whether the ring is fully connected. A graph database becomes worth discussing only if drafts grow so much that the in-memory pass no longer fits a laptop, or if many people need live queries over a continuously edited network.

I wrote docs/graph/DECISION.md and changed nothing else in the repo.
