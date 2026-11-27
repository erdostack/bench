# Roast: db/ (rebuild.sql, planner.sql, schema.sql) and jobs/rebuild.py

Verdict: Nothing serious. The HIGH on db/rebuild.sql line 3 is not a defect: the DELETE with no WHERE is the full rebuild, and the INSERT that follows it sits in the same BEGIN IMMEDIATE transaction. Adding a WHERE would keep withdrawn routes in hop, which the README forbids, so the SQL should not change for this finding. The MEDIUM on planner.sql line 5 is also not a defect: the walk terminates. Four low notes remain, all questions about data the repo does not contain.

Judged against:
- Engine: SQLite in WAL mode, one file on the planner hosts (README.md; db/schema.sql line 1). Checked here on SQLite 3.53.1 through Python 3.13.
- Workload: stop, trip and stop_time are loaded by the importer (not in the repo); hop is rebuilt nightly after the importer; the planner reads hop while the rebuild runs (README.md).
- Invariants: times keep counting past midnight, and a later stop never has an earlier time because the importer rejects such a feed (README.md lines 5 to 7). A route the operator withdrew must disappear from hop (README.md line 12).
- Size and planner budget: not stated.
- Scanner: SQL-DEL-001 (HIGH, db/rebuild.sql:3) and SQL-REC-003 (MEDIUM, db/planner.sql:5) from scan/report.txt.

## Findings

### low: `seq`
A gap in the sequence silently drops a hop.
Problem: db/rebuild.sql joins the next stop with `b.seq = a.seq + 1`. A gap in seq (for example 1, 2, 4) drops the hop across the gap, with no error. The schema (db/schema.sql) does not require contiguous values, and the README does not say they are. Not evidenced in the shipped files; a question to confirm.
Fix: Confirm the importer writes seq as 1..n per trip, and document it. Better: join on the next stop by order, for example with LEAD(seq) per trip_id, so gaps cannot drop a hop.

### low: `service_day`
The rebuild ignores the service day the trip table records.
Problem: trip has `service_day TEXT NOT NULL`, but db/rebuild.sql reads every trip row regardless of it. The README says hop matches tonight's timetable. If the importer keeps trips for more than one service day, hop mixes days. The importer is not in the repo, so this cannot be confirmed here.
Fix: Confirm the importer keeps only tonight's service day. If not, filter trips to tonight in db/rebuild.sql and document it in the README.

### low: `jobs/rebuild.py`
The nightly job does not check what the importer left behind.
Problem: jobs/rebuild.py runs db/rebuild.sql without checking that the importer succeeded or that stop_time and trip are not empty. The DELETE and INSERT commit together, so an empty or partial stop_time commits an empty or partial hop with no error. The README says the importer rejects a bad feed, but not what it leaves in the tables when it does.
Fix: Before the rebuild, check the importer's exit status and that stop_time has rows, and abort if either fails. A failed check leaves last night's hop in place.

### low: `earliest_arrival`
The walk keeps every (stop, minutes) state within the budget, so cost grows with the budget.
Problem: planner.sql's recursive CTE keeps every (stop_id, minutes) state within :budget, not one best row per stop. Routes run both ways, so the data has loops with positive hop times, and the intermediate rows grow with the budget; the cost is not bounded in the file. It terminates for any finite budget (checked on SQLite 3.53.1 with a 3-stop loop and budgets of 60 and 100000; row counts were not measured). The README does not state a budget range.
Fix: Cap :budget in the caller at a documented maximum window. If longer windows are needed, use a per-stop best-time search (Dijkstra in the application, or one row per stop). A depth counter does not fix this, because termination already holds.

## Holds up
- `db/rebuild.sql` DELETE FROM hop (scanner SQL-DEL-001, HIGH): the statement is the rebuild, not a stray delete. Checked here: a failed INSERT (a CHECK violation on minutes) raised an error, and hop kept its 3 rows, so the transaction rolled back. A WHERE would leave withdrawn routes in hop, which the README forbids. No change to the SQL. The finding should be closed as accepted with this reason, not by editing the statement. Adding a condition that is always true (for example WHERE 1 = 1) would pass the scanner without changing behaviour, and would hide the intent, so it is not recommended.
- Readers during the rebuild (README.md lines 13 and 14): checked here in WAL mode. A second connection still saw the old 3 rows while the writer held BEGIN IMMEDIATE with the DELETE applied, and saw the new row only after COMMIT.
- `earliest_arrival` recursion (scanner SQL-REC-003, MEDIUM): the scanner says it may not terminate. It does: UNION discards repeated (stop, minutes) rows, and every positive hop adds time, which the WHERE on :budget caps. Checked with a loop containing 0-minute and 3-minute hops. The depth counter the scanner recommends is not needed. The cost question is kept as the low finding above.
- `stop_time` primary key (trip_id, seq) (db/schema.sql line 11): serves the b.seq = a.seq + 1 join and the trip lookups on its leading column. `hop` primary key (from_stop, to_stop, route_id) leads with from_stop, which serves hops_from and the recursive join in planner.sql.
- `hop` CHECK (minutes >= 0) (db/schema.sql line 17): consistent with the importer rule that a later stop is never earlier, so the rebuild's min never hits the check on a valid feed.

## Not checked
- The importer, its deletion of withdrawn routes, and its service-day and seq rules are not in the repo. The README's withdrawn-route guarantee depends on them, and was not verified.
- db/planner.sql names :budget but the repo does not set it, so the budget range was not checked.
- No production data, row counts or timings were available. The loop and rollback checks used a 3-stop sample on SQLite 3.53.1.
- The scanner's rule text was not compared with the rule's own definition.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
