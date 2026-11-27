# schoolrun-routes

Carpool routes for the district's primary schools, in Neo4j 5.26. A route is the ordered list of
stops a carpool drives on its school run; the drivers' map and the parents' "where is the car" view
read it.

- `db/changes/`: change files, applied in order by the release pipeline (`docs/changes.md`).
- `docs/routes.md`: how routes are stored.
- `ci/`: CI output.
