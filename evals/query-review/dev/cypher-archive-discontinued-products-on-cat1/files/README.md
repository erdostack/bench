# merchgraph

The merchandise catalogue graph: products, brands, ranges and suppliers. Website search, the app and
the supplier portal read it.

- `bin/mq <server> "<cypher>"` or `bin/mq <server> --file <file>`: run Cypher on a server from `config/servers.toml`.
- `changes/`: data changes, `YYYY-MM-DD_<slug>.cypher`.
- `docs/`: the server and the change rules, and the model.
