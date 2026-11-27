# ops

- `compose/graph.yaml`: the development graph database. `make up` uses this file.
- `compose/app.yaml`: the API container, for testing the image locally: `docker compose -f ops/compose/graph.yaml -f ops/compose/app.yaml up`.

Passwords are read from the environment. Put `export CURIO_GRAPH_PASSWORD=...` in `ops/compose/local.env.sh`
(ignored by git) and source it.
