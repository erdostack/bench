# pantry-pairs

The ingredient-substitution graph behind the recipe app's "out of buttermilk?" hints:
`(:Ingredient)-[:SUBSTITUTES_FOR {ratio}]->(:Ingredient)` and `(:Recipe)-[:USES]->(:Ingredient)`.

## Local cluster

`npm run dev` starts Skaffold, which installs the Helm chart in `deploy/chart` on your local Kubernetes with
`deploy/values-local.yaml` (Neo4j 2026.07.1) and forwards Bolt to localhost:7687. The password comes from the
`pantry-graph-auth` secret (see `deploy/README.md`).

## Queries

    npm run cypher -- queries/substitutes_for.cypher
    npm run seed                                  # loads data/*.json; needs a fresh database
