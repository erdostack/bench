Decision: recursive-sql

For now nothing moves: on 39 of 40 tenants the recursive query is 6 ms p95 against a 3 s budget. But this is
provisional: the enterprise tenant has never been timed, and by Sanne's rule a miss there means the graph store.
Please get the query timed on the enterprise tenant before anyone builds on this. Notes in notes/role-inheritance.md.
