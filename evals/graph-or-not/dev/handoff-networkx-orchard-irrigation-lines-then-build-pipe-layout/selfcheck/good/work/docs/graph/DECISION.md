# Orchard pipe plan

Decision: in-process-library

## Workload facts (from the conversation, 2026-11-23)

- New block: 212 valves, 1,900 candidate trench runs. Plan redone a few times a year.
- networkx minimum spanning tree: about 20 ms, 9% less trench than the current nearest-next walk in
  irrigation/layout.py.
- Contractor's rule: boring under the farm track costs about as much as 40 m of trench, so a run with
  crosses_track = 1 costs length_m + 40 when choosing runs.

## Options considered

- graph-database (GIS vendor): rejected; a server for an occasional script.
- in-process-library: chosen; networkx minimum_spanning_tree.
- recursive-sql: rejected; not a traversal.
- no-graph: rejected; the walk is the problem.

## What would change the decision

- Pipe sizes or pressure limits per run: then it is a network design problem, still in-process.
