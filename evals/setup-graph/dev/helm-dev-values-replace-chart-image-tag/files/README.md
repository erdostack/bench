# partsbin

Bill-of-materials explorer for a small workshop: every assembly, the parts it is built from, and the question that
comes up every week, "if this bracket is discontinued, what stops shipping?"

## Stack

- TypeScript on Node 22
- Graph database: Neo4j 5.26 (LTS), deployed with the Helm chart in `deploy/chart`
- No ORM; the queries live in `queries/` as `.cypher` files

## Getting started

    npm ci
    make dev-up          # installs the chart into a local kind cluster
    make forward         # bolt on localhost:7687
    npm run cq -- queries/where_used.cypher part=BRK-220

`npm run cq` runs a saved query in a read transaction and prints a table.
