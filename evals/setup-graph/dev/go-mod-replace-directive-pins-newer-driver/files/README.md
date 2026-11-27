# fibremap

Fibre cables, cabinets and exchanges of a generated town network, and the queries that find single points of
failure.

- Neo4j 2026.02.2 (compose.yaml; credentials in .env)
- Go 1.24, neo4j-go-driver v5.20.0 (go.mod)
- `make q F=queries/single_points.cypher`
