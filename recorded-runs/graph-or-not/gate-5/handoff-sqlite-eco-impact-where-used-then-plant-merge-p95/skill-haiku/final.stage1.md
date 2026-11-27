Decision: recursive-sql

No change is needed now. Under the rule you and Ines agreed, the impact screen stays on the recursive query while its p95 is under 800 ms. Your stated p95 is 180 ms over about 600 opens a day, roughly 4.4 times headroom, so the networkx move is not triggered and the contractor's graph database is not indicated by these numbers.

Numbers the decision turns on:
- Present p95: 180 ms against the 800 ms threshold (your figure; the repo holds no timing and no production data).
- Load: about 600 opens a day, 4.21 BOM lines per item on average (400,000 lines over 95,000 items).
- Ana's prototype, 350 MB and 20 ms (your figure, not run here), shows the fallback is viable if the threshold is ever crossed.

What I could not find or measure: the real BOM depth and fan-out, the number of routes against the distinct assemblies reached (the query uses `UNION ALL` with a path column, so it returns one row per route, which can waste work on a dense BOM), the production plan and timing on the replica, and how the 180 ms was measured. I ran the repo's loop test on SQLite and it passed.

What would change this: a production p95 above 800 ms over a stated window (then move the walk to networkx in the ECO service, as agreed), or a route count far above the distinct assemblies, which would point to a rewrite of the walk before any move.

Nothing in the repo was changed. The decision record is at `docs/graph/DECISION.md`.
