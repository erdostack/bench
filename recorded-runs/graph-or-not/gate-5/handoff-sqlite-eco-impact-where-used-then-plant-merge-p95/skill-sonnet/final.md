Still stands: no

The decision was recursive-sql. It is now in-process-library (networkx in the ECO service), and docs/graph/DECISION.md is updated.

The numbers it turns on:
- Impact screen p95: 180 ms before the merge, 1.3 s now. The rule you and Ines agreed last spring is to stay on recursive SQL while p95 is under 800 ms, and past that to move the walk into memory with networkx. 1,300 / 800 = 162.5% of the limit, so the trigger is met.
- BOM lines: 400,000 before, 1.1M now, which is 2.75 times as many. Latency grew about 7.2 times (1,300 / 180) for that growth.
- Ana's prototype held the BOM in 350 MB and answered in 20 ms, at the 400,000-line size. Scaled linearly to 1.1M lines that is about 960 MB. That is my estimate, not a measurement.

A graph database is not the answer. The agreed rule names networkx as the next step, and nothing shows the BOM is too big for one process.

What I did not find or measure:
- There is no copy of the database in the repo, so 1.3 s is your figure and I did not re-measure it.
- I don't know the memory per ECO service process or how many copies would run, so I can't say whether about 1 GB per copy fits.
- I don't know how stale an in-memory copy may be, or the write rate.
- I don't know the item count or the BOM depth after the merge.
- Ana's prototype has not been re-run on the merged data.

The first step is to re-run Ana's prototype on the 1.1M merged lines and check memory and reload time. I did not run the `UNION` rewrite of the where-used query, which carries only the item id. It could win time back, but nobody has run it, so the file lists it as a remedy to measure.

Only docs/graph/DECISION.md was changed. I wrote no code, dependency or migration changes.
