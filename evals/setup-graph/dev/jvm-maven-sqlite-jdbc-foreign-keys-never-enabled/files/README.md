# gridline

Substations and transmission lines of a generated regional grid, kept in SQLite (data/grid.db). Feeder paths
and islanding checks are recursive CTEs in sql/.

- Run one: `bin/sql sql/feeders_of.sql`
- Take a substation out of service: `bin/decommission <id>`

The schema's foreign keys keep every line attached to substations that exist, so the CTEs don't need to check
for dangling ends.
