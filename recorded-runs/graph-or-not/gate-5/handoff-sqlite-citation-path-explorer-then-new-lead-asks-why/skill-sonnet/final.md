Decision: graph-database

We decided to move the citation-path explorer to a dedicated graph database and not leave it on the SQLite snapshot. The choice is gated by a trial on the full edge set with the real filters before any money is committed. The record is `docs/graph/DECISION.md`.

What the explorer does: it finds the shortest citation chains between two papers, up to 6 hops, in either direction. It skips retracted papers, and optionally goes only through papers after a given year. Those filters apply during the walk, not afterwards. The data is 410M citations between 96M papers, 400 staff use it, and the budget is 3 s p95. New citations arrive at about 1.2M a day and must be visible the next morning.

Why not stay on SQLite, as Marisol suggests: it was measured and failed.
- The recursive query in `sql/path.sql`, with indexes on both ends of the citation edge, ran at 41 s p95 on a copy of the snapshot. The budget is 3 s, so that is 13.7 times over (41 / 3). Better indexes are not the fix, because both directions are already indexed (`citation_cited` plus the primary key).
- A closure table, the usual SQL way to make this fast, came out at about 90 billion rows. That is about 220 rows for every one of the 410M edges (90B / 410M), so it is not a remedy.
- The average fan-out is 4.3 citations per paper (410M / 96M). Searching both ways gives about 8.6 per step, and over 6 hops that can reach roughly 8.6^6, about 400 million papers. That is the same order as the whole graph, which is why walking it in SQL is so slow.

Why not load it in memory instead (the other cheap option):
- networkx on a 20M-citation sample took 2.6 GB. Scaled to everything that is 2.6 GB x 20.5 = about 53 GB per worker. `citepath/paths.py` loads the whole graph in every worker, and there are 6 workers (`citepath/config.py`) on 32 GB hosts.
- Wen's compressed numpy array fits in 6 GB and runs a search in 0.8 s, which is a real result. But 6 workers each holding a copy is 6 x 6 = 36 GB against 32 GB. Every new filter took her about two weeks to add. The platform team also said no to running it, and a rebuild for the daily changes takes 40 minutes.

The costs of the graph database are a second stateful system to run, a daily feed from the snapshot, and a new query language. A graph database does not remove the hub problem (very highly cited papers), so the 6-hop limit and any cap on hubs should stay.

Gaps and what would change the call. The record is clear that the array is the close second place. If Wen's array were held once per host (shared between the 6 workers, 6 GB against 32 GB), measured at 3 s p95 or under with the real filters at 400-staff load, and the platform team accepted the 40-minute nightly rebuild, the decision would move to an in-process library. A rewritten SQLite query measured at 3 s p95 or under on the snapshot copy would move it back to recursive SQL. Today it is 41 s. Neither has been shown. The SQLite rewrite remains the cheaper thing to try first if Marisol wants it tested, but the record does not treat it as holding until someone runs it.

What the record does not know: the real concurrency at peak, how often the year filter is used, latency by hop count (only one p95 exists), and which graph engine. Nothing was measured when I read the record for this, and I changed nothing in the repo.
