Decision: recursive-sql

1.2M BOM lines is a modest table for Postgres. Keep sql/where_used.sql, which already walks any depth, and run it
for the changed components in batches. No graph database and no second copy of the BOMs in the planner.
