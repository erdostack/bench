Decision: recursive-sql

Keep the BOM in SQLite and compute the rolled-up unit cost with a depth-limited recursive query. A graph database is not needed, and it would not make the references real: the dangling lines come from the ERP load, not from the storage engine.

- The walk costs about 0.1 ms per quote at the stated scale, measured on synthetic data (200 walks in 16 to 20 ms). At 200 quotes a day that is about 20 ms of database time per day.
- The orphan rule fits the SQL walk: a `LEFT JOIN` to `item` marks an assembly incomplete when any reached component has no item row, so the quote page can show it as incomplete instead of a partial total.
- Enabling `PRAGMA foreign_keys` now would make the load fail on the roughly 300 orphan lines, so do not turn it on until those lines are resolved.

Open items before go-live: run the depth-7 walk on a copy of the real export, because the repo holds only 6 items and the synthetic shape is an approximation; count how many assemblies each orphan line affects; and get the quote page's latency budget from its owner.

Full evidence, the options considered and what would change the decision are in `docs/graph/DECISION.md` in the working directory. Nothing in the repo was changed except that new file.
