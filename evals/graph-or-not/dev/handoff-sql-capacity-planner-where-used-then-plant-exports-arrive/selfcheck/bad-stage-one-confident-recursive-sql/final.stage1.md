Decision: recursive-sql

Stay on Postgres. A recursive query is the right tool for a where-used, and Kai's graph database is not needed.
Batch the 40,000 components into one query per run instead of one per component.
