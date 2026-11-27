Decision: in-process-library

Keep the circles page in the application and walk the attendance data in memory. Neo4j is not needed for this. The whole network is 18 women and 139 pairs who share an event, read from a CSV that never changes. I measured it: from any of the 18 women, every other woman is reached within 2 steps, so the "step by step out to the whole network" view has only two layers of depth for this data.

Why not the other options:
- Neo4j would be a second server to run on a small shared host, for a static graph of this size.
- Recursive SQL needs a SQL database that the site already runs. None exists here, so it would mean adding one.
- No graph does not fit: the first layer is a plain list of direct connections, but the layers beyond it need a walk.

networkx 3.7 is already pinned in requirements.txt, so the library route needs no new dependency. A plain dictionary and a breadth-first loop would also do.

What would change this: a much larger or live-updated dataset, or a site database that already exists and could hold the same two-step walk. Neither applies to the current exhibit.

Full write-up: /run/work/docs/graph/DECISION.md. I changed nothing in the repo except that file.
