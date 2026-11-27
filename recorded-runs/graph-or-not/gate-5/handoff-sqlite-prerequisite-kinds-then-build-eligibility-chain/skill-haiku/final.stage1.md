Decision: recursive-sql

Keep the catalogue in SQLite and run the list as a recursive query. The walk is short and the table is small: 3,900 prerequisite rows, a longest chain of 7, and about 0.035 page views a second on average. On a synthetic catalogue of the same shape, the query matched an independent check for all 2,400 courses and finished in a median of 0.01 ms per course. A worst case that reaches every course took a median of 13 ms. A graph database would add a second system and an import step for that load.

The query must do three things. It follows only required and concurrent rows, so recommended edges and anything reached only through them are never walked. It uses UNION on the course id, not on a hop count, so the 23 cross-listed loops terminate. It excludes the starting course from its own result.

Not known: the share of recommended rows in the real export, the peak view rate, whether each cross-listed pair is exactly two rows, and the latency budget for a page. The timings are from synthetic data, not the registrar's file, so run the query on the real catalogue before release.

Nothing in the repo was changed except the new file docs/graph/DECISION.md.
