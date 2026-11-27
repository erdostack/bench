# storenet

The store network graph: stores, the companies that operate them, regions and formats. Finance, the
estates team and the store finder use it.

- `bin/sq <server> "<cypher>"` or `bin/sq <server> --file <file>`: run Cypher on a server from `config/servers.toml`.
- `changes/`: one file per data change, `NNN-<slug>.cypher`.
- `docs/`: servers and the change process, and the model.
