# wagongraph

The rail freight wagon fleet as a Neo4j graph: wagons, their owners and keepers, the depots that maintain
them and the allocations of wagons to customer flows. The allocation screen and the maintenance planner
read it.

- `bin/wg <target> "<cypher>"` / `bin/wg <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `changes/`: reviewed data changes, `NNNN-<slug>.cypher`.
- `queries/`: saved read queries used by the screens.
- `docs/`: model and targets.
