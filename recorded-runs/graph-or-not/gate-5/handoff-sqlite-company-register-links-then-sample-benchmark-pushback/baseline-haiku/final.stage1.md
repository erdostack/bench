Decision: graph-database

Adopt a dedicated graph database for the 6-link and mixed-kind questions, and keep SQLite as the system of record for the weekly import.

Why:
- It is the only option with a measured result under the 10 s limit: the two-week Neo4j trial answered the same 6-link questions in 2 to 8 s on a copy of the data.
- The SQLite options measured far outside the limit: linked_within at 6 hops ran 14 minutes before it was killed, and the best level-by-level search from both ends took 3 min 20 s. The hub addresses and company-formation agents with hundreds of thousands of links are the cause, and they hurt any naive expansion.
- The in-process library is ruled out by memory: about 95 GB for a 64 GB server, and a fixed algorithm would not cover new questions anyway.
- Analysts wrote their own patterns after one day in Neo4j, which the current canned-query setup does not allow.

Caveats before the budget round:
- The 14-minute figure comes from linked_within in investigate/queries.py. That query is a recursive CTE that carries a path string per row and checks only that path, so it enumerates every simple path up to 6 hops and does not share a visited set across rows. The slowdown is in the query shape as much as in SQLite. A frontier-based search with a global visited table might be much faster. It has not been measured, so Wim's tuning idea is not ruled out, but the only measured route under 10 s is the graph database.
- The Neo4j numbers cover only 6-link questions and were measured on a copy. The trial does not say whether the copy was the full 310M-relation set, whether caches were warm, or how questions mixing relation kinds and date ranges performed. Confirm these before committing budget.
- Keep the SQLite import as the source of truth and load it into Neo4j on each weekly run, so the graph store can be rebuilt rather than maintained by hand.

Suggested check (cheap, and worth it before the budget round): rerun the 6-hop question on the full SQLite file with a frontier-based BFS and a global visited set, and time the same date-filtered, mixed-kind questions on Neo4j. If the SQL version comes in under 10 s, reconsider recursive-sql.
