# 0009: store for register links

Status: accepted (2026-11-24)

Decision: graph-database

48M entities, 310M relations. Budget: answer in under 10 s. Full-data runs: recursive CTE killed at 14 min;
bidirectional level-by-level 3 min 20 s. networkx ~95 GB vs 64 GB. Neo4j trial: 2 to 8 s.
