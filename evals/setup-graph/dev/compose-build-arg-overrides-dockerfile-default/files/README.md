# depotwalk

Pick-route planner for a small warehouse: bins, the aisles that connect them, and the shortest walk that visits
every bin on a pick list.

## Run it locally

    export DEPOTWALK_GRAPH_PASSWORD=<choose one>
    make graph-up
    make load
    make cq FILE=queries/neighbours.cypher
    go run ./cmd/server

## Repository map

| Path | What |
|---|---|
| `cmd/server` | HTTP API |
| `cmd/cq` | runs one saved query and prints rows |
| `cmd/load` | loads `data/` into the graph |
| `internal/` | planner and graph access |
| `infra/graph` | the database image |
| `queries/` | saved Cypher |
