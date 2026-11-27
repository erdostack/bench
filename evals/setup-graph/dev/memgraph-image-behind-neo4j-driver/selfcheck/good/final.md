Wrote docs/graph/CONTEXT.md. Worth knowing: the code uses the neo4j Python driver, but the database in docker-compose.yml is Memgraph 3.5.0, not Neo4j, so queries have to be written for Memgraph.
