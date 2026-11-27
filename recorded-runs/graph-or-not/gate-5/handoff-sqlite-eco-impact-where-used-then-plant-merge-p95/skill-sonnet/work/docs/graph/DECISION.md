# Graph decision

Decision: in-process-library

The question was whether the ECO board's impact screen still belongs on recursive SQL after the Ostrava plant's BOMs were merged into PLM. It does not: the impact screen is now at 1.3 s p95 (was 180 ms), over the 800 ms trigger that you and Ines agreed last spring, so the agreed rule moves the where-used walk into the ECO service's memory with networkx. A graph database is not called for.

## Workload facts

- The question asked of the connections: every assembly that uses a changed part at any level, a walk upward along `bom_line` of data-dependent depth (sql/where_used.sql, ecoboard/impact.py).
- Walk form: a recursive CTE with `UNION ALL`, carrying a path string, and `path NOT LIKE` to stop loops, then `GROUP BY` with `MIN(lvl)` to list each assembly once. It produces one row per route, not one per assembly (sql/where_used.sql). This is wasted work that a rewrite carrying only the item id with `UNION` would remove; nobody has run that rewrite, so it does not reopen the question (see below).
- Loops: PLM imports have produced loops from bad imports (stated by the user); tests cover a loop and check each assembly is listed once (tests/test_where_used.py).
- Indexes: `bom_line_component` on component_id serves the upward step, primary key (parent_id, component_id) (db/schema.sql).
- Size now: 1.1M BOM lines after the Ostrava merge (stated by the user), up from 400,000 before it (stated by the user earlier, recorded here); 1,100,000 / 400,000 = 2.75 times as many lines. Item count now: unknown (was 95,000 before the merge, stated by the user). Fan-out before the merge was 400,000 / 95,000 = about 4.2 BOM lines per item (derived); after the merge it is unknown for the same reason.
- Load: the screen is opened about 600 times a day (stated by the user, before the merge; not restated since); 600 / 8 hours = about 75 an hour (derived, assuming an 8-hour working day).
- Measured latency now: 1.3 s p95 on the impact screen (stated by the user, not re-measured here; no database copy in the repo, var/ is git-ignored). Before the merge it was 180 ms p95 (stated by the user). 1,300 / 180 = about 7.2 times slower for 2.75 times the lines.
- The team's own rule: stay on this query while the impact screen's p95 stays under 800 ms, and past that move the walk into the ECO service's memory with networkx, not a graph database (stated by the user, agreed with Ines, the DBA, last spring). 1,300 ms is 162.5% of 800 ms (1,300 / 800); the trigger is met. Before the merge 180 ms was 22.5% of it.
- Prototype: Ana's prototype held all of the BOM in 350 MB and answered in 20 ms (stated by the user), at the 400,000-line size. Scaled linearly to 1.1M lines that is about 350 x 2.75 = 962 MB (derived; assumes memory grows with BOM lines, not measured at the new size). It describes the remedy, not today's workload, and has not been re-run on the merged data. networkx 3.7 is already in requirements.txt (requirements.txt).
- Memory per process of the ECO service and number of processes: unknown (not in the repo), so whether about 1 GB per copy fits is not yet known.
- Writes and freshness: unknown; the service reads the PLM replica (Postgres 16) (README.md), and no write rate or required staleness is stated.
- What is operated today: PLM replica on Postgres 16; tests run on SQLite from db/schema.sql; queries in sql/ run on both (README.md).
- What was already tried: unknown beyond the loop-safe rewrite already in place; the repo holds no decision records or bench notes.
- unknown: the depth of the BOM data and the depth of requests; maximum (not just p95) latency; growth of the BOM beyond the Ostrava merge.

## Options considered

- graph-database (a dedicated graph store, as the PLM contractor pitches for "engineering knowledge"): rejected, because the agreed rule names networkx, not a graph database, as the next step, and the BOM (1.1M lines, about 1 GB scaled from Ana's prototype) is not shown to be too large for one process or too fast-changing for a copy per process.
- in-process-library (networkx in the ECO service): chosen, because recursive SQL now measures 1.3 s p95 against the 800 ms rule (was 180 ms), so the agreed trigger is met, and Ana's prototype held the BOM in 350 MB and answered in 20 ms at 400,000 lines. The size at 1.1M lines, memory per process and the reload time are not measured, so the first step is to re-run the prototype on the merged data.
- recursive-sql (recursive queries on the PLM replica, Postgres 16): rejected, because it has been measured failing the agreed limit, 1.3 s p95 against 800 ms, and a rewrite nobody has run does not reopen that.
- no-graph (plain joins, no traversal): rejected, because where-used at any level follows parent-component links of unknown depth, which needs a walk.

## What would change the decision

- Ana's prototype re-run on the 1.1M merged lines needing more memory than one ECO service process can hold, times the number of copies it would run (the service owners set the limit), or a reload of the in-memory copy that cannot meet the freshness the ECO board needs (the board sets it), would move this to graph-database, or back to recursive-sql if a measured rewrite fits.
- A measured run of the `UNION` rewrite (carrying only the item id, one row per assembly rather than per route) on the merged data coming in under 800 ms p95 would move this back to recursive-sql; until it is run it is a remedy to measure, not a verdict.
- The impact screen's p95 falling back under 800 ms for another reason, such as a changed rule agreed with Ines, would move this back to recursive-sql.
