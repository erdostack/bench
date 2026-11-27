# shopgraph

Recommendation queries for the storefront. Neo4j 5, read replicas behind the product page.

`neo4j/schema.cypher` has the constraints, `neo4j/recs.cypher` the queries (each one starts with `// name:`).

## What is in the graph

| Thing | Count | Notes |
|---|---|---|
| `Customer` | 14 million | |
| `Product` | 1.2 million | |
| `Category` | 3,400 | about 350 products each |
| `Country` | 9 | one node per market; the largest has 5.8 million customers attached |
| `BOUGHT` | 210 million | `Customer` to `Product`, with `at` |
| `VIEWED` | last 30 days only | `Customer` to `Product`, with `at` |
| `LIVES_IN` | 14 million | `Customer` to `Country` |
| `IN_CATEGORY` | 1.2 million | `Product` to `Category` |

## Where the queries run

Every query in `recs.cypher` runs while a product page is being rendered, once per page view, and has to
come back within 100 ms.
