# hublane

Parcel tracking for a regional carrier. The graph is Neo4j 5.

    model/schema.cypher    constraints and indexes
    model/writes.cypher    the statements the scanner service runs
    model/reads.cypher     the read queries; each has a `// name:` line

## Workload

- `depot_backlog` is the dispatch screen in every depot: the parcels waiting there, oldest first. It is
  polled by about 900 screens, roughly 400 calls a second in the morning, budget 40 ms.
- `parcel_trace` is the customer tracking page.
- `route_manifest` is printed once per route per day.
- `depot_load` runs once a night per depot for the capacity report.

## How parcels move

A parcel is registered at the depot that receives it. About 70% of parcels then pass through one or two
more depots before they go out for delivery: each arrival scan runs `move_parcel`.

## Notes on the model

- `Parcel.depot_code` repeats the code of the depot the parcel is `AT`. It was added in May so that
  `depot_backlog` can be answered from the `parcel_depot_status` index; going through the `Depot` node
  meant reading every parcel that had ever been at a big depot. The write statements keep it in step with
  the relationship.

## Size

| Thing | Count |
|---|---|
| `Parcel` | 38 million, 310,000 new a day |
| `Depot` | 64 |
| `Route` | 5,200 a day |
