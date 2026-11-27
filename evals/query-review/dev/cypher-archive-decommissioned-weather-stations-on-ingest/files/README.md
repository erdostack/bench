# stationgraph

The weather observing network as a Neo4j graph: stations, their sensors and the regions they report for.
The ingest service writes observations against it, and the public observations API and the forecasters'
station map read it.

- `bin/sg <target> "<cypher>"` / `bin/sg <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `changes/`: reviewed data changes, `NNNN-<slug>.cypher`.
- `queries/`: saved read queries used by the map and the API.
- `docs/`: model and targets.
