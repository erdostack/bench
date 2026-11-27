# yardgraph

Tractors, trailers and chassis of the Coldwater fleet, and who pulled what (`coupling`), as a graph in
SQLite. Schema in `db/schema.sql`. Jobs in `jobs/` are run by the scheduler with `run(conn)` on
`var/fleet.db`. Fleet rules: `docs/fleet.md`.
