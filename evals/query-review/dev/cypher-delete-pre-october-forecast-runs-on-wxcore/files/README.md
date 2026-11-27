# forecast-store

Point forecasts from the numerical weather prediction runs, stored as a Neo4j 5.26 graph: each model run,
the model it came from, and its forecast for every station in the network. The verification jobs and the
forecasters' comparison screen read it.

- `bin/fx <target> "<cypher>"` / `bin/fx <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `changes/`: reviewed data changes, `<nnn>_<slug>.cypher`.
- `docs/`: model, retention and targets.
