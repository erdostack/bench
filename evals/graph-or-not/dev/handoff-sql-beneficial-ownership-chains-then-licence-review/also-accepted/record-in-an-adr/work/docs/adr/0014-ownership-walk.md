# ADR 0014: ownership walk on a graph database

Decision: graph-database

48M companies, 61M holdings, 24 deep, cycles. Budget 800 ms p95. Recursive SQL 4.6 s; closure table ~2.1 billion
rows; networkx ~70 GB vs 32 GB hosts.
