Decision: graph-database

The citation-path explorer has to return chains of up to 6 citations in 3 s p95 for 400 staff, over 410M citations and 96M papers. The recursive query runs at 41 s p95 on a copy, about 13.7 times the budget, so it is measured failing. The in-memory options do not fit as deployed: six workers with a 6 GB array each need 36 GB on a 32 GB host, and networkx would need about 53 GB per worker. A graph database is the choice on this evidence. Two cheaper trials could still overturn it, and they should run first.

1. Rewrite `sql/path.sql` to stop at the meeting depth, use a visited set in place of the path string, and apply the year and retraction filters during the walk. Replay real searches on a copy against 3 s p95. If it passes, the answer is recursive SQL and Sanne's plan stands.
2. Share one memory-mapped copy of Wen's array per host across the six workers. If it meets 0.8 s with the filters on and the daily rebuild fits the refresh window, the answer is an in-process library. The platform team's objection to the rebuild would need a fresh answer.

If neither passes, the graph database is the choice, and the cost is a second stateful system, a daily ingest of about 1.2M citations, and a new query language.

Nothing in the repository was changed except the new file `docs/graph/DECISION.md`.
