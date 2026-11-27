# dockflow

Rebalancing questions over a generated bike-share network: docks, and a RIDES_TO link with the average
rides per day from one dock to another.

Graph database: Neo4j 5.26, the service container in `.github/workflows/graph-job.yml`, which loads the
data and runs every query in queries/ each night. Locally, point NEO4J_URI at any Neo4j you have running.

    make load                               # go run ./cmd/load data
    make q F=queries/drain_chains.cypher    # go run ./cmd/q <file>
