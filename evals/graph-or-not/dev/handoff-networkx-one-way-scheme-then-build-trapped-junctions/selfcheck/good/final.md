Rewrote trapped_junctions in oneway/trapped.py with networkx, per docs/graph/DECISION.md: road segments only, one-way
directions followed, and a junction is trapped unless it can both reach the ring road and be reached from it. No
step cap, so the long one-way loop is no longer flagged; footpath-only junctions are not in the graph, so they are
not reported.
