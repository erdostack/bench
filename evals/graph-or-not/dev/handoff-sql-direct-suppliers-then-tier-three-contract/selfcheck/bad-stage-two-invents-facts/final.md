Still stands: no

The report used to need tier 1 only, over about 2M supply rows, run hourly. Tier 3 is a walk of up to three hops, so
it needs traversal now; on 2M rows a recursive query on Postgres does it. Decision line updated to recursive-sql.
