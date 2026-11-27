# ran-graph

The radio access network inventory as a Neo4j graph: cell sites, their sectors and the carriers each
sector transmits. Read by the planning tool, alarm correlation and field dispatch.

- `bin/rg <target> "<cypher>"` / `bin/rg <target> --file <f>`: run Cypher on a target in `config/targets.toml`.
- `bin/migrate <target>`: apply pending files in `migrations/` (`V<NNN>__<what>.cypher`) in order.
- `docker compose up` starts a local Neo4j 5.26 for `ran-scratch`, loaded from the nightly dump.
- `docs/model.md`: the graph model. `docs/operations.md`: targets and how changes reach them.
