Verdict: do not wire connected_closures into the outage tool yet. `queries/connected_closures.sql` never finishes on plant.db.

The recursive walk matches each span at either end, so it steps straight back along the span it came by. Each step adds to the hop count, so UNION never removes a repeated closure. With a 5-second cap, a run from closure N-0000 (id 1) was interrupted without a result. The correct answer is 1,300 closures, up to 52 hops. The comment saying the walk cannot come back to a reached closure is wrong.

Fix (tested read-only on SQLite 3.53.1 against a BFS over the same spans, 42 starting closures, same results, worst run 0.03 seconds): keep a visited path and prune revisits. The statement is in the ROAST.md and in findings.json. It relies on the no-rings rule in the README, which the data satisfies.

Everything else is sound: the indexes cover the lookups, span_report counts correctly, and customers_on uses its index.

Not checked: other SQLite versions, the query plan, the outage tool's timeouts, and whether the writer enforces the declared foreign keys (the repo does not show the writer).

Files:
- /run/work/docs/graph/ROAST.md
- /run/work/findings.json
