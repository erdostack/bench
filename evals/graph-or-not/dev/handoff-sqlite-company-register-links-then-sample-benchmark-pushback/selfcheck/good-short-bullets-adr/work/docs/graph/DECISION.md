# linkfinder: where the register's links should live

Decision: graph-database

## Workload facts (from the owner, 2026-11-24)

- Full register: 48M entities, 310M relations of 11 kinds; a 41 GB SQLite file on a 64 GB analysis server.
- 25 analysts, new ad-hoc questions every day (up to 6 links, mixing relation kinds and dates); an answer is needed
  in under 10 s.
- Measured on the full data: linked_within at 6 hops killed after 14 minutes (indexes and path check in place);
  level-by-level search from both ends, one query per level: 3 min 20 s. Hubs (addresses, formation agents) have
  hundreds of thousands of links.
- networkx estimated at about 95 GB, and it is one fixed algorithm.
- Two-week Neo4j trial on a copy: the same 6-link questions in 2 to 8 s; analysts wrote patterns after a day.

## Options considered

- recursive-sql (Wim): tuned and measured; 14 min and 3 min 20 s against 10 s.
- in-process-library: does not fit (95 GB on 64 GB) and does not serve ad-hoc questions.
- graph-database: chosen; measured inside the budget in the trial.

## What would change the decision

- Analysts' questions settling into a few fixed shapes that a precomputed table could answer.
