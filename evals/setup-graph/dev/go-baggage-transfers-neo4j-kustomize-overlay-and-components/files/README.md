# bagtrace

Graph of the hub's baggage transfers: flights, bag tags and the belts and sorters a bag passes on its way
between flights. We use it to find bags at risk of missing a connection and the sorter that delays most
transfers.

## The graph

Neo4j 5.26.24 LTS (`deploy/base/statefulset.yaml`), run in the team's dev namespace on the shared cluster.
The dev overlay only adds a small volume. Loads come from the baggage system's hourly export and are done
by the ingest job, not from this repo.

    make up        # apply the dev overlay
    make forward   # port-forward bolt to localhost:7687
    make q F=queries/missed_connections.cypher

Credentials come from the `graph-auth` secret; `make forward` prints how to export them.
