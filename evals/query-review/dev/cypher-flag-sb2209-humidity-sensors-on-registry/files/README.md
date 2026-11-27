# sensor-registry

The register of every sensor in the weather observing network, as a Neo4j 5.26 graph: sensors, the
stations they are installed at, and the stores that hold spares. Field crews' job lists, the asset audit
and the calibration planner read it.

- `bin/reg <target> "<cypher>"` / `bin/reg <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `changes/`: reviewed data changes, `CR-<nnnn>-<slug>.cypher`.
- `queries/`: saved read queries (crew job list, audit extracts).
- `docs/`: model and targets.
