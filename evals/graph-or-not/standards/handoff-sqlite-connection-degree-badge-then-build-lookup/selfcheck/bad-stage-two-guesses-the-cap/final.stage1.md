Decision: recursive-sql

A walk of at most three steps over 610,000 friendships fits SQLite with the two indexes on knows; Neo4j would be a
second store for a bounded lookup at 30 views a second.
