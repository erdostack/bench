# parcelroute

Depot-to-depot routing for a regional courier. The graph holds depots and the trunk lines between them;
custom procedures in `plugin/` compute the cheapest hand-off chain inside the database.

    docker compose up -d --build       # builds docker/neo4j/Dockerfile (procedures included)
    scripts/run-query.sh queries/handoffs.cypher

See docs/design/procedures.md for the procedures.
