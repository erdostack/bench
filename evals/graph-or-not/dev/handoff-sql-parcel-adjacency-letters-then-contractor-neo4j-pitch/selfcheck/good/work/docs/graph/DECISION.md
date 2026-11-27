# Neighbour letters for permit applications

Decision: no-graph

## Workload facts (given by the owner, 2026-11-23)

- Letters go to the owners of every parcel adjacent to the application's parcel. First ring only: the bylaw is
  explicit, never neighbours of neighbours.
- Adjacency is precomputed nightly by the GIS team into parcel_adjacency: 480k parcels, 2.7M adjacency rows.
- About 150 applications a week, letters sent as one batch on Monday mornings.
- Measured: the lookup for one application on the replica, 3 ms.

## Options considered

- graph-database (the GIS contractor's pitch): rejected. A nightly copy of PostGIS data for one join a week.
- in-process-library: rejected. Nothing to walk.
- recursive-sql: not needed. One ring is a join.
- no-graph: chosen.

## What would change the decision

- The bylaw changing to more than one ring (then a bounded recursive query on the same table).
