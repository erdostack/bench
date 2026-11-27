# bandgraph

Musicians, bands and recording sessions from a generated discography: who played with whom, and the shortest
chain of sessions between two players.

- Graph store: Memgraph, `docker compose up -d`
- Client: Neo4j Java driver 5.13.0 over Bolt
- `make q F=queries/session_chain.cypher`
