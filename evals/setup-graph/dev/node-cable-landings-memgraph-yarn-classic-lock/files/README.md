# cablemap

Submarine cable systems and their landing stations as a graph in Memgraph:
`(:Cable)-[:LANDS_AT]->(:Station)-[:IN]->(:Country)`. Client: neo4j-driver 5.12.2 (Memgraph speaks Bolt).

    docker compose up -d
    yarn install
    yarn q queries/redundancy.cypher country=PT

The data is refreshed by the import job in the infra repo; this repo only reads.
