# shopgraph

The web shop's product graph: products, categories, brands and what goes with what.

- `bin/gq <server> "<cypher>"` or `bin/gq <server> --file <file>`: run Cypher on a server from `config/servers.toml`.
- `migrations/`: reviewed changes for live, `NNN_<slug>.cypher`.
- `fixtures/`: what the dev graph is loaded from.
- `docs/`: servers, the model.
