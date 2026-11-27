# Graph decision

Decision: in-process-library

The question is whether the diversion checker needs a graph database, a graph library in the worker, recursive SQL, or no graph at all. The regional extract has now arrived with 180,000 segments and 150,000 junctions, which is under the 800,000-segment bound recorded before; the network held in one worker's memory comes to about 332 MB against the 1.5 GB limit, and a measured check on a synthetic network of that size met the 2 s budget with a median of about 0.9 s, most of it in the edge scan. This is a decision on the arithmetic and a synthetic measurement, so the real extract must pass one trial in one worker before go-live.

## Workload facts

- Regional extract: 180,000 segments and 150,000 junctions (stated by the user). Previously recorded as unknown; this replaces the open count. About 1.2 segments per junction.
- Worker memory limit: 1.5 GB, hard (stated by the user).
- Check latency budget: 2 s per check (stated by the user).
- Check rate: about 300 checks per day (stated by the user), about 12.5 per hour on average; a low, batch-like rate per worker.
- Pilot county sample: 38,000 segments (stated by the user); the prototype holds the network in about 70 MB and a route takes 30 ms (stated by the user; not measured by this agent).
- Per-segment memory at pilot scale: 70 MB / 38,000 = about 1,840 bytes per segment (derived; assumes the 70 MB is the network load and scales linearly with segments; earlier record used the same figure).
- Regional memory, pilot rate: 180,000 x 1,842 B = about 332 MB, about 22% of 1.5 GB (derived; extrapolation from the pilot figure).
- Regional memory, measured: load(conn) of 180,000 synthetic segments into the MultiDiGraph gave 244.8 MB traced after load, 1,360 bytes per segment (measured: tracemalloc around load() in a scratch script, the synthetic data built in SQLite memory; not the real extract, and not the same as the pilot's 70 MB, which the repo does not explain). Either figure leaves most of the limit free.
- One process holds one copy; a reload that builds a second copy while the first is live: about 664 MB at the pilot rate (derived: 2 x 332 MB). Copies per deploy: unknown.
- Edge scan cost, measured: diversion() at 38,000 synthetic segments: scan median 170 ms of a 172 ms check; at 180,000 segments: scan median 805 ms of an 889 ms check (measured, 30 closed segments, weight 20 t, scratch script). A second run at 180,000 segments gave a median of 998 ms and a maximum of 1,449 ms, with 13 of 30 checks finding a path (measured, same method). The scan is about 2.5 microseconds per edge (805 ms / 324,066 directed edges, derived), so its cost grows with the whole network, not the route.
- Margin against the 2 s budget on this machine: about 2.2x at the median and about 1.4x at the slowest measured check (derived from the measurements above). The measurements use a synthetic grid, not the real road network, and this machine is not the platform's.
- The pilot's reported 30 ms per route (stated by the user) is far below the 172 ms measured here at pilot size; the two figures are not reconciled, so the regional time is taken from the measurements, not from the reported figure.
- National product: about 4 million segments (stated by the user). Its load at pilot cost: 4,000,000 x 1,842 B = about 7.4 GB, about 4.9 times the 1.5 GB limit (derived; extrapolation). The worker holds the regional extract, so this is the far end of the range, not the expected size.
- Graph structure: segments connect junctions with from_j and to_j, travel minutes, a weight restriction and a oneway flag (db/schema.sql). The prototype builds a MultiDiGraph (roads/diversion.py) and runs Dijkstra with a cost that drops segments below the vehicle's weight limit.
- Freshness: the extract is replaced when delivered (README.md); the reload cadence and freshness requirement are not stated.
- Dependency: networkx 3.7 (requirements.txt). Runs as a worker on the permit platform (README.md).
- var/roads.db is absent from the working copy (var/ is gitignored), so the real row counts, plan and timing could not be taken.
- unknown: the real extract's attributes beyond the six columns in the schema, its connectivity, the real route mix and weight classes; the real traced memory; route time on the real extract and platform hardware; freshness requirement; number of worker copies and reload cadence; whether the platform can host a graph database service.

## Options considered

- graph-database (a dedicated graph store, Dan's proposal; the product is not named in the repo): rejected for now, because the regional network fits one worker's copy at about 332 MB (derived) and the measured check at that size meets the 2 s budget, so the need is met without a second stateful system to run and feed. Dan's proposal would be re-examined only under the conditions below.
- in-process-library (networkx in the worker, the network held in memory): chosen, because it is the first option whose evidence meets the need: about 332 MB derived and 245 MB measured for the loaded graph against a 1.5 GB limit, and a median check of about 0.9 s against the 2 s budget on a synthetic network of the regional size. The gate before go-live is the real extract loaded in one worker with the real route query, measuring traced memory and per-check time.
- recursive-sql (recursive queries on SQLite): not shown to hold. No SQL route has been measured at this size, and a shortest path with a weight limit is a search that a recursive query does not express directly; it is not needed while the in-process route meets the budget.
- no-graph (plain joins, no traversal): rejected, because the check is a shortest path through the network.

## What would change the decision

1. The real extract, loaded in one worker, gives a per-check time above 2 s on the real route mix. First remedy: replace the closed-segment scan with an index from segment_id to its ends, which removes the scan that is most of the time measured here; re-measure. Owner of the 2 s budget: the permit service.
2. Traced memory of the real extract after load above about 750 MB (half the 1.5 GB limit, so that a reload copy still fits), or any measured growth in the attributes the check keeps. Owner of the 1.5 GB limit: the permit platform team.
3. The worker must hold the national network (about 4 million segments, about 7.4 GB at pilot cost, derived). Then in-process-library is out, and the choice is between recursive-sql (after a measured trial) and graph-database.
4. Copies per worker or reload cadence that puts more than one live copy per process beyond what the platform allows; with about 332 MB per copy, a second copy during reload is about 664 MB. Owners: the platform team and the supplier.
5. graph-database would move here only if the network does not fit one worker's copy, a SQL route is measured failing the 2 s budget at regional scale with the failure count and its total, and the platform can host a database service. Dan's proposal stays unsupported until then.

Nothing in the repo was changed beyond this file.
