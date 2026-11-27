# haulplan

Depot-to-depot routing for a regional haulier: depots, the legs between them, and which legs are closed today.

The graph backend runs in Docker (see `docker-compose.yml`) and speaks Bolt, so the application uses the stock
`neo4j` Python driver; there is no ORM in between.

    docker compose up -d
    pip install -r requirements.txt
    scripts/mgq.sh queries/open_route.cypher
