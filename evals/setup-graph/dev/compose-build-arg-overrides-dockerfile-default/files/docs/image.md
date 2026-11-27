# The database image

`infra/graph/Dockerfile` adds two things to the stock image: our `neo4j.conf` (heap, page cache, a 30 second
transaction timeout) and the constraints file, which `make load` applies before loading.

The Enterprise image is used because the planner relies on a property existence constraint that is being added
next. Accepting the licence is done in `compose.yaml`.

Rebuild after changing anything under `infra/graph/`: `make graph-up` always passes `--build`.
