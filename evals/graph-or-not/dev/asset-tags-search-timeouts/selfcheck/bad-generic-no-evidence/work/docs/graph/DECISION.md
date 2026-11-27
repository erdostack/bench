Decision: recursive-sql

Tag hierarchies are small. PostgreSQL handles them with recursive CTEs, so a graph database is
unnecessary. Make sure the join columns are indexed.
