Decision: recursive-sql

Keep the tree page on the existing recursive query in `sql/ancestors.sql`, and change nothing now. At 18 ms p95 (your measurement) it is well inside the graduate school's 250 ms budget and well under the 120 ms point you and Tomasz agreed would trigger a graph database review. Its 41,000 researchers and 46,500 advising rows are a small graph, and the query already handles loops with its path check and its 30-generation cap.

Why not a graph database yet: the agreed trigger is not met, and a graph server would add a second system and a nightly feed to a page that already meets its budget. "Genealogies are graphs" describes the shape of the data but does not on its own show a need. That is the same reasoning for the in-memory option, which would add a load step the page does not need.

What to watch, in order:

1. The tree page's p95 on production. If it goes above 120 ms, that is the point to look at a graph database properly.
2. The national dissertations register. Its size and share of co-advised dissertations are not known here. Load a copy at the expected size and time the query before the register lands, not after.
3. Route count. The query uses `UNION ALL`, so it returns one row per route, not per researcher. That is harmless at today's size, but count the rows on a copy at the national size. If they grow far beyond the researcher count, rewrite the query to `UNION` on the researcher id before looking at any other tool.

What I could not check: `var/lineage.db` is not in the repo, and `lineage/build.py`, which the README names, is not there either. The 18 ms figure is your measurement and could not be re-run here. Nothing in the repo was changed except the new file docs/graph/DECISION.md.
