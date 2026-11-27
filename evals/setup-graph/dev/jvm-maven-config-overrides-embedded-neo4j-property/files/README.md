# citeweave

A citation graph of a generated paper corpus (data/corpus/*.jsonl), stored in embedded Neo4j 5.26.24 (the
pom property `neo4j.version`). There is no server: the store lives in data/store/ and is opened in process.

- `bin/load` rebuilds data/store/ from the corpus files
- `bin/cypher queries/most_cited.cypher` runs one saved query in a read transaction
