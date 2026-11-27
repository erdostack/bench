# reelgraph

The film catalogue graph behind the streaming front end: titles, people, territories, viewers and
their ratings.

- `bin/rq <server> "<cypher>"` or `bin/rq <server> --file <file>`: run Cypher on a server from
  `config/servers.toml`.
- `changes/`: one file per change to catalogue data, `YYYY-MM-DD_<what>.cypher`.
- `queries/`: the shelves and reports.
- `docs/`: servers, the model, and the rules for changes.
