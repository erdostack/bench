Decision: recursive-sql

Kemal is right. Postgres handles this with a recursive CTE over knows and the index on person2_id; 120 ms is plenty. No Neo4j.
