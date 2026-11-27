# Roast: hopgraph db/ (schema.sql, rebuild.sql, planner.sql, jobs/rebuild.py)

Verdict: Nothing serious, and nothing to change in `db/rebuild.sql`. The DELETE without a WHERE is the point of the file: a nightly full rebuild of a derived table, in one transaction. Adding a WHERE would make it worse, because a route the operator withdrew would stay in `hop`. Mark the HIGH as a documented exemption instead (reason below). The MEDIUM on `db/planner.sql` is also safe as written.

Judged against:
- Engine: SQLite, WAL mode, one file on the planner hosts (README.md); version not stated. I ran the statements on the SQLite bundled with the local Python.
- Derived table: `hop` is "derived entirely from `stop_time` and `trip`; nothing else writes it" (README.md).
- Refresh: `jobs/rebuild.py` runs `db/rebuild.sql` every night after the importer, so `hop` "always matches tonight's timetable", and "a route the operator withdrew must disappear from `hop`" (README.md).
- Concurrency: the planner reads `hop` while the rebuild runs; WAL gives it the old graph until the rebuild commits (README.md).
- Data: times are minutes from the start of the service day and never go backwards along a trip; the importer rejects a feed where they would (README.md). Row counts, hop count and query rate: not stated.
- Release rule: no open HIGHs; scan from 2026-11-20 (scan/report.txt).

## Findings

None.

An audit tool shouted HIGH at a nightly full rebuild and asked for a WHERE clause, a request that would have turned a working design into one with ghost routes. Both warnings are the scanner reading syntax rather than the README. The schema survives the roast, which should worry everyone.

## Holds up
- `db/rebuild.sql` (the `DELETE FROM hop;` at line 3, scan SQL-DEL-001, HIGH): the delete removes every row because the next statement recomputes every row, and `BEGIN IMMEDIATE` ... `COMMIT` makes it one atomic step. Under WAL the planner keeps reading the old `hop` until the commit, so nobody sees an empty graph. No row of `hop` is source data (nothing else writes it, README.md), so nothing is lost: if the script fails midway, the transaction is rolled back when `jobs/rebuild.py` closes the connection, and the old graph stays. A WHERE that "targets only the intended rows" has no right answer here: any filter that keeps rows leaves stale ones, and the README says a withdrawn route has to vanish. I ran it on a toy timetable: a hand-inserted `hop` row for a route not in the timetable was gone after the rebuild. The right change is to accept the finding with this reason (an exemption on that line, with the README sentence as justification), and not an edit. A `WHERE 1 = 1` would silence the scanner and change nothing; it is up to you whether to want that as a stopgap, but it is not a fix for anything.
- `db/planner.sql` `earliest_arrival` (scan SQL-REC-003, MEDIUM): the walk is bounded by `WHERE r.minutes + h.minutes <= :budget`, and `UNION` removes repeated rows. A cycle with positive minutes runs out of budget; a cycle of zero-minute hops (allowed by `CHECK (minutes >= 0)` in `hop`) returns the same `(stop_id, minutes)` row and is dropped. I ran a loop of zero-minute hops (A to B to A) with a budget of 50 and it finished. The reachable set is capped by stops times budget. A depth counter would be extra insurance, not a repair; not needed unless callers can pass an unbounded `:budget`, which no file shows.
- `hop` `PRIMARY KEY (from_stop, to_stop, route_id)`: matches the `GROUP BY a.stop_id, b.stop_id, t.route_id` in the insert, so one row per pair and route; and `WHERE from_stop = :stop` in `hops_from` and the recursive join on `h.from_stop` lead with the key (WITHOUT ROWID table), so both are index searches.
- `stop_time` `PRIMARY KEY (trip_id, seq)`: serves the self-join on `b.trip_id = a.trip_id AND b.seq = a.seq + 1`, and `trip.id` serves the join to `trip`.
- `hop.minutes` `CHECK (minutes >= 0)`: guards the derived value; a bad timetable makes the rebuild fail and roll back, keeping the previous graph.

## Not checked
- Row counts and runtime of the nightly rebuild and of `earliest_arrival` at real size: not stated, and a toy database only shows correctness.
- The importer is not in the repo, so the README's "importer rejects a feed where times go backwards" is taken as stated; the `CHECK` on `hop.minutes` is the only guard visible here.
- Whether the release process allows a documented exemption for a HIGH, and how your scanner records one: I cannot see its configuration.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
