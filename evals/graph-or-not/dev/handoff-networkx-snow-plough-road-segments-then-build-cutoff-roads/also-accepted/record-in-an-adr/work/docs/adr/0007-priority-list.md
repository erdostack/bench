# Plough priority list

Decision: in-process-library

## Workload facts (from the conversation, 2026-11-23)

- Export: 2,300 junctions, 3,100 segments; run every autumn and after big roadworks.
- networkx bridges: 31 segments with no way round, about 0.2 s. The current winter/cutoff.py lists 54 because its
  detour search stops after 8 hops, so long loops look like dead ends.
- Highways manager's rule: a segment goes on the list ONLY if closing it cuts at least one house (junction.houses)
  off from the depot (junction 1). Dead ends to a car park, the quarry etc. with no houses do not count.
- Two roads can join the same junctions (schema comment); they are separate segments.

## Options considered

- graph-database (GIS team): rejected; a server for an annual script.
- in-process-library: chosen; networkx.
- recursive-sql: rejected; bridges are not a recursive query.
- no-graph: rejected; the answer is about alternative routes.

## What would change the decision

- Live closures during a storm, rerouting ploughs in real time.
