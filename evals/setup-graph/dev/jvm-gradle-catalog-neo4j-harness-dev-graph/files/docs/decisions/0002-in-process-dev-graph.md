# 0002 In-process dev graph

Status: accepted

We dropped the shared dev server. Each run starts its own Neo4j inside the JVM through neo4j-harness,
loads the fixture and throws the database away afterwards, so nobody's experiment leaks into anybody
else's. The harness version follows the server version, which keeps the dev graph on the same Neo4j as
the hosted one the library network uses.
