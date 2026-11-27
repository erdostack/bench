# kerbside-graph

The trip graph of a ride-hailing service, in Neo4j 2025.10: riders and drivers are nodes, every trip
is a `RODE_WITH` relationship from the rider to the driver, and a rider's rating of a trip is a
`RATED` relationship.

- `db/changes/`: change files, applied by the release pipeline (`docs/changes.md`).
- `docs/ratings.md`: how ratings are stored.
