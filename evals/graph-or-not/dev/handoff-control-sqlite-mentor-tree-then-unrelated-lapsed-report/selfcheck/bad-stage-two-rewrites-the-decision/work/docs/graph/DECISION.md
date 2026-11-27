# Mentor lines

Decision: graph-database

Workload (2026-11-23): about 9,000 volunteers; mentor chains at most 8 deep; about 30 lookups a day from the admin
page; one SQLite file; two volunteer maintainers.

Rejected: graph database (a server to run for 30 lookups a day); in-memory graph library (works, but buys nothing
over one query); no-graph (chains vary in depth).
