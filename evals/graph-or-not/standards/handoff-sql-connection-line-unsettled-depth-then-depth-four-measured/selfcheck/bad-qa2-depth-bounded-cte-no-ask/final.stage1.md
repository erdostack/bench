Decision: recursive-sql

Kemal is right: shortest path length is a textbook recursive CTE over knows (both directions, depth-bounded). Postgres handles this; no Neo4j.
