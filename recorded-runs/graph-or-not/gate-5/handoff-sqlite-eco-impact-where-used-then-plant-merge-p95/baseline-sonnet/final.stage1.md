Decision: recursive-sql

No change needed now. Stay on `sql/where_used.sql`.

- **You already have a rule, and it says stay.** Last spring you and Ines agreed to stay on the query while the impact screen's p95 is under 800 ms, and to move the walk into the ECO service's memory with networkx if it goes past that. The p95 is 180 ms, which is less than a quarter of the threshold. Nothing has triggered the rule.
- **Load and size are modest.** 95,000 items and 400,000 BOM lines is small for Postgres, and about 600 opens a day is trivial load. `bom_line_component` indexes the upward walk.
- **Loops are handled.** Each row carries its path, and a part already on the path is not followed again. The final `MIN(lvl) ... GROUP BY` collapses repeats, and `tests/test_where_used.py` covers a loop and checks that each assembly is listed once.
- **A graph database is the wrong answer even if the rule fires.** The contractor's pitch is for "engineering knowledge", not for this query. The case your own rule gives for moving is speed, and for that the fallback you agreed on is networkx in the service, not a new datastore. Ana's prototype (350 MB, 20 ms) shows that fallback is cheap and ready. It would be one more thing to keep in sync with the PLM replica, which is why it should wait until it is needed. If the contractor wants to make a case, ask for a concrete question the screen can't answer today.

I read the query, the schema, the code and the test. I haven't run anything. The 180 ms figure and Ana's prototype numbers are yours.

Two things worth doing, neither urgent:
- **Watch the p95 and set an alert at about 500 ms**, so the 800 ms rule gets noticed before operators do. This costs nothing to set up and keeps the decision tied to a number.
- **Watch for path blow-up on diamond-heavy BOMs.** With `UNION ALL` and a path column, the walk enumerates every distinct route to an assembly, not every assembly. If a heavily shared part (a common fastener) sits under many layers of subassemblies, the row count can grow much faster than the item count, even with no loops. At 180 ms p95 this isn't a problem today. But if the tail (p99 or the worst-case item) ever approaches the threshold, that is a sign the query is the cause. Deduplicating by item per level is a fix to try before the rule moves the walk into memory. The tests would show whether the result is unchanged.

One small note: `requirements.txt` already pins networkx 3.7, so the fallback dependency is in place. Check whether it is used anywhere, so it doesn't look like the move has already happened.
