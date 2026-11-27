# ADR 0021: yank-impact check

Decision: graph-database

History: accepted 2026-11-23 as in-process-library (networkx in the registry service, 6 GB, 38 ms p95; MySQL
recursive 2.4 s, budget 500 ms) with the rule: in-process while it fits in half a 32 GB host. Superseded
2026-11-30: 21 GB resident after the mobile merge (33M edges); moving to a graph database.
