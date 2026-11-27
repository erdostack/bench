# parceltrace

Parcel tracking for the Northline network. Scans (`scan`) record a parcel arriving at a hub; the
`leg` table is the hub-to-hub edge list derived from consecutive scans, which the network planners
query as a graph. Schema in `db/schema.sql`.

Jobs in `jobs/` are run by the scheduler with `run(conn)` against `var/parcels.db`. See `docs/jobs.md`.
