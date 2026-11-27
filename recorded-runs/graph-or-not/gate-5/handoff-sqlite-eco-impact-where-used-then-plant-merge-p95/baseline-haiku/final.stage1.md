Decision: recursive-sql

No change is needed now. Keep `sql/where_used.sql` on Postgres, and don't adopt a graph database. Your agreed rule is met with room to spare: the impact screen's p95 is 180 ms against an 800 ms threshold, which is about 4.4 times headroom. Under the rule as agreed with Ines, you stay on the query until p95 crosses 800 ms, and it hasn't.

Why the query fits this load: `where_used.sql` walks the bill of materials upward from the changed part, with the `bom_line_component` index supporting each step. A path check stops it following a part already on its own path, so PLM loops terminate. The screen runs about 600 times a day, so the load is light. The contractor's case for a graph database for "engineering knowledge" is not supported by this screen's needs. The screen answers one question, where-used, and the graph database would add a second store to sync with PLM for no measured benefit.

Two things to watch, not decision drivers:
- The query enumerates paths, not parts. It is `UNION ALL` with a per-path check, so the row count is the number of distinct upward paths, which can be far larger than the number of assemblies in a dense or diamond-shaped BOM. The p95 on latency may stay flat until it suddenly does not. Track the row count from `up` per run alongside p95, so you see the growth before the 800 ms threshold trips.
- `requirements.txt` already pins `networkx==3.7`, but the impact path doesn't use it. Ana's prototype (350 MB, 20 ms) is the fallback if the threshold is crossed, as agreed. Nothing is needed now.

The test `tests/test_where_used.py` covers the loop case and should stay in place. If you change the query, rerun it, and rerun the timing against the production replica, not only the SQLite test database.

Revisit if p95 goes above 800 ms (then move the walk to networkx, as agreed), or if the path-count trend shows the enumeration growing faster than the item count.
