        # dockside

        Bike-share fleet graph: stations, bikes, trips, workshop jobs. Neo4j; the ops console reads it
        through the JavaScript driver. `queries/` holds one statement per file, parameters and columns in the
        header; `tests/smoke.sh` runs every file against a target with the sample parameters in
`tests/params.json`, then rolls back.

        Local development: `docker compose up` (see `docker-compose.yml`).
