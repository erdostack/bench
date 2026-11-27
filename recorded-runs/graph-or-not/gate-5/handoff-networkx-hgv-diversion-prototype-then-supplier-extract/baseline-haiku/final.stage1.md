Decision: need-more-information

The choice depends on one number nobody has yet: the segment count of the regional extract. The prototype's memory use scales with it, and the worker's limit is hard.

The arithmetic, assuming memory grows roughly linearly with segments (not yet measured at scale):
- Pilot: about 70 MB for 38,000 segments, so roughly 1.8 KB per segment.
- Worker limit: 1.5 GB. At 1.8 KB per segment, that is about 800,000 segments before any headroom. Allowing for the Python and networkx baseline and a safety margin, a safe in-process ceiling is probably 400,000 segments or fewer. That figure is my estimate, not a measurement.
- National product: about 4 million segments, which at the same rate is roughly 7 GB. That does not fit in the worker under any reading.

What would decide it:
- If the regional extract is comfortably under the ceiling, the in-process library is the right choice. Measure peak memory on a file of that size, not steady state, before relying on it.
- If it is above the ceiling, do not load the network into the worker. Then a graph database (or a routing service) that holds the graph outside the worker is the candidate. That answers Dan's point about memory, but it adds a service to run and a network call to fit inside the 2 s budget, so it should be chosen on those costs, not as a default.
- Recursive SQL is a poor fit here. The check is a weighted quickest route that respects weight limits and one-way streets. Recursive queries enumerate paths well but do not do weighted shortest paths idiomatically, so this would be a lot of custom SQL for little gain.

Before production, regardless of the answer:
- Ask the supplier for the segment count and file size of the regional extract now, rather than waiting for delivery.
- `diversion()` finds the closed segment by scanning every edge (`g.edges(keys=True)`). That is linear in network size on every check. At 38,000 segments it is harmless; at millions it would alone threaten the 2 s budget. Keep a lookup from segment id to its endpoints, built once.
- `load()` rebuilds the whole graph. Make sure the worker loads it once and reuses it across checks, not once per check.
- Nothing was run. There is no `var/roads.db` in the workspace, so the 70 MB and 30 ms figures are the ones you gave me, not measurements I made.
