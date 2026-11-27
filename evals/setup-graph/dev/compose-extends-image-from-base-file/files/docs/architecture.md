# Architecture

The service is a plain Java 21 application. All state is in one graph database: Neo4j 2025.10.1
(see compose.yaml). We use the official Java driver and keep every query in `queries/` so that it can
be reviewed on its own.

## Data flow

1. Mill and finisher exports arrive as CSV in `import/`.
2. `Loader` merges them as `(:Lot)-[:PROCESSED_AT]->(:Site)` and `(:Lot)-[:CUT_FROM]->(:Lot)`.
3. Recall queries walk CUT_FROM backwards to find every lot that shares an origin.
