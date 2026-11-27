# haulage

Tanker routes and collection points of the Northmoor Milk Group. The data lives in SQLite files named in
`config/targets.toml`; `bin/coopdb <target> "<sql>"` or `bin/coopdb <target> --file <file>` runs SQL on a
target. Read `docs/ENVIRONMENTS.md` before running anything. Schema: `db/schema.sql`.
