# routing

Depot-to-depot route planning on the shared Memgraph instance (`memgraph` in the root `compose.yaml`).

    pip install -r requirements.txt
    make -C ../.. up
    scripts/mgq.sh queries/next_hop.cypher

`scripts/mgq.sh` pipes a Cypher file into `mgconsole` inside the container. The service itself connects with
`pymgclient`.
