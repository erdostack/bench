# pollinet

Plant-pollinator visits from generated field surveys, as a bipartite graph in Memgraph: which plants share
pollinators, which pollinators are generalists.

- Memgraph 3.5.0 (compose.yaml)
- neo4j-go-driver v5.28.1 (go.mod), talking Bolt to Memgraph
- `make q F=queries/shared_pollinators.cypher`
