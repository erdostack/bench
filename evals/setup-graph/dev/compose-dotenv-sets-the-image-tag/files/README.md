# tidewatch

Relay planning for a mesh of coastal buoys. Each buoy forwards readings to its neighbours until one of
them reaches a shore station; the graph tells us which buoys have only one way home.

## Requirements

- Docker with Compose v2
- Go 1.24

The graph is Neo4j 5.26.24 Community (the LTS line), started with `make up`.

## Use

    make up                         # start the graph
    make seed                       # load db/seed.cypher
    make q F=queries/relay_paths.cypher

The model is described in docs/model.md.
