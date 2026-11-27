# member-graph

Meadowside Energy Co-operative's member register as a graph: members, the sites they hold shares in,
general meetings, and referrals. Neo4j 5.26 on every server.

- `bin/rg <server> "<cypher>"` or `bin/rg <server> --file <file>`: run Cypher on a server from `config/servers.toml`.
- `changes/`: reviewed data changes. `docs/`: the model and the servers.
