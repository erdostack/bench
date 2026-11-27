# seedvault

Accession records and the lineage graph of a community seed bank. An accession is a batch of seed; when a batch
is regrown, the new accession `(:Accession)-[:GROWN_FROM {year, site}]->(:Accession)` points at its parent.

- PostgreSQL keeps the accession records and germination tests (`app` module).
- Neo4j keeps the lineage graph (`lineage` module). Write queries as described in docs/query-style.md.

```
docker compose up -d
./gradlew :lineage:cypher -Pfile=queries/descendants.cypher
```
