# spokes

Bikes, docking stations and operators of the shared bicycle scheme as a Neo4j 5.26 graph, and the queries
the rider app's map and filters use.

- `bin/sk <target> "<cypher>"` / `bin/sk <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `fixtures/seed.cypher`: the data the `dev` database is built from.
- `changes/`: reviewed data changes for prod, `NNNN-<slug>.cypher`.
- `docs/`: targets and the model.
