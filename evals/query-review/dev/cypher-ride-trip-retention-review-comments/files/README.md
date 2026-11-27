# kerbside-graph

The trip graph of a ride-hailing service, in Neo4j 2025.10: riders and drivers are nodes, every trip
is a `RODE_WITH` relationship from the rider to the driver.

- `db/changes/`: change files, applied in order by the release pipeline (`docs/changes.md`).
- `docs/model.md`: labels, relationships and properties.
- `docs/retention.md`: what is kept and for how long.
