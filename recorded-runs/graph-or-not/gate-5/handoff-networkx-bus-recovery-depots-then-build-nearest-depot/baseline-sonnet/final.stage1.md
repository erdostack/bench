Decision: in-process-library

Keep networkx, which the app already uses. This is a bug in how the graph is built and queried. It is not a reason to change architecture.

What was wrong, in `recovery/nearest.py`:
- `shortest_path_length` had no `weight`, so it counted segments instead of minutes.
- `load` added bus-gate segments, so the lorry could route through them.
- For parallel segments, `add_edge` on a plain `Graph` overwrites, so the last row won. That is the bug you spotted.

What I changed:
- `load` now reads only `bus_gate = 0` segments.
- When two segments join the same junctions, `load` keeps the lower `minutes`.
- `shortest_path_length` now uses `weight="minutes"`.

Check: I ran a toy network where the quick bus gate is the last row between two junctions. The old road is slow and a longer detour is faster overall. The function now picks the depot reached by the detour. I did not run it against the real `var/roads.db`, which is not in the repo. I did not add a test file to the repo.

Why not a graph database or recursive SQL: 6,200 junctions, 8,100 segments, 4 depots and about 30 queries a day is tiny. Dijkstra over that in memory takes milliseconds. Reloading the graph on every call, as `nearest_depot` does now, is the only real cost. If it matters, cache the graph or use one multi-source Dijkstra from the depots. I didn't change that. A vendor-hosted graph database would add a second copy of the road data to keep in sync and would not fix this bug. The routing rules (vehicle class, minutes) would still need to be right.

Open question: `minutes` is "typical driving time". If the control room wants time-of-day or live traffic, that is a data question and doesn't change the decision.
