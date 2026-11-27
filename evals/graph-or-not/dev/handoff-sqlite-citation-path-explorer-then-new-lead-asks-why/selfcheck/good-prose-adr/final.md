Decision: graph-database

We moved the path search to a graph database (ADR 0006). The SQLite recursive query was measured at 41 s p95 against the office's 3 s budget, and networkx would need about 53 GB per worker on 32 GB hosts.
