# kerbside-graph

The trip graph of a ride-hailing service, in Neo4j 2025.10: riders and drivers are nodes, every trip
is a `RODE_WITH` relationship from the rider to the driver. Safety (shared-ride patterns), fraud
(collusion rings) and driver earnings read it.

- `loader/`: the nightly import of the previous day's trips (`docs/loader.md`).
- `docs/model.md`: labels, relationships and properties.
