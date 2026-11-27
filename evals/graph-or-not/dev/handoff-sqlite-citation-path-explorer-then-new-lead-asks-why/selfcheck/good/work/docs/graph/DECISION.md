# Citation-path explorer: where the path search lives

Decision: graph-database

## Workload facts (from the conversation of 2026-11-24)

- 410M citations between 96M papers; about 1.2M new citations a day, visible next morning.
- Search: shortest chains between two papers, up to 6 hops, skipping retracted papers, optionally only through
  papers after a given year. Budget **3 s p95**, 400 staff.
- Measured: recursive query (sql/path.sql, indexes both ways) **41 s p95**.
- networkx: 2.6 GB for a 20M sample, about **53 GB per worker**; 6 workers on **32 GB hosts**.
- Numpy adjacency array (Wen): 6 GB, 0.8 s, but about two weeks per new filter, 40-minute rebuild for daily changes;
  the platform team declined to run it.
- Closure table: about 90 billion rows.

## Options considered

- recursive-sql (Sanne: stay on SQLite with better indexes): rejected, 14x over budget with indexes already there.
- in-process-library: rejected, does not fit the hosts; the bespoke array was refused by its operators.
- graph-database: chosen; filtered variable-length paths are what it is for.

## What would change the decision

- Search depth cut to 2 hops, or hosts with several hundred GB per worker.
