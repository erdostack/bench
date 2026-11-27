# loyaltygraph

The loyalty programme's offer graph: members, the personalised offers issued to them, and the products
an offer applies to.

- `bin/lq <server> "<cypher>"` or `bin/lq <server> --file <file>`: run Cypher on a server from `config/servers.toml`.
- `changes/`: one file per change to offer data, `NNNN_<slug>.cypher`.
- `docs/`: servers and how changes are made, and the model.
