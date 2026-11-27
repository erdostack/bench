# Graph decision

Decision: recursive-sql

Sign-off has to follow the solid reporting line up from the submitter's own manager until the first person at grade 7 or above, over 6,400 employees and 7,900 reporting lines, at most 12 levels deep. A recursive query on the SQLite export the service already reads fits. Each employee has at most one solid manager, so a trace is one single path of at most 12 rows, not a search.

## Workload facts

- Question asked of the connections: a walk up one relation between employees (employee to line manager), to a data-dependent depth, stopping at the first grade 7 or above (stated by the user; hr/approvals.py TODO). Nothing walks today: `reporting_lines()` in hr/approvals.py reads one employee's lines.
- Counts: 6,400 employees, 7,900 reporting lines of which about 1,500 are dotted, chains at most 12 levels deep (stated by the user).
- Rules agreed with Finance, not negotiable (stated by the user): only solid lines count and a dotted-line lead never signs anything; the chain goes up from the submitter's own manager and stops at the first person who is grade 7 or above, who is the last approver, and nobody in between is skipped.
- Loop rule (stated by the user): the export has loops since the March re-org was half applied, Lena found 23 of them (people who end up as each other's line manager). When the chain comes back to someone already in it, including the person who submitted, it stops there and HR ops picks the claim up by hand.
- Export is a 3 MB SQLite file, regenerated once an hour (README.md); the approval page is opened about 200 times a day (stated by the user) = 200 / 86,400 = about 0.002 per second, about 1 every 7 minutes on average. Peak rate unknown.
- Solid lines: 7,900 - 1,500 = about 6,400 (stated counts, subtracted), which matches one per employee (about 1 solid line each, the top person having none). db/schema.sql enforces it: the unique partial index `reporting_line_one_solid` allows at most one solid line per employee.
- Bound on required work: the solid chain from one person is a single path, at most 12 steps deep and so at most 12 rows (stated depth, plus the unique index). With a loop, the walk stops on the first repeat, so it is still at most 6,400 rows even if the depth claim were wrong. Each step is a primary-key lookup on `employee` plus an index lookup on `reporting_line(employee_id, ...)` (db/schema.sql).
- What is operated today: SQLite through the standard library, Python 3.11+, no other dependency (README.md, hr/approvals.py). `grade` is on `employee` (1 to 9).
- Tried before: nothing recorded. The repo has no decision record, usage export, slow-query log or migration history.
- unknown: any timing (there is no copy of the export in the repo, *.db is gitignored, so nothing was run or measured). Peak request rate. Whether the 12-level depth holds in the half-applied March data (the loop rule covers it either way).

## Options considered

- graph-database (Neo4j, as Jonas proposes): rejected, because the work per request is one path of at most 12 rows, over about 6,400 solid lines, about 200 times a day, on an hourly export. A second stateful system with its own hourly feed buys nothing here, and the loop and grade 7 rules are the same ones to write in any engine.
- in-process-library (export loaded into memory, for example a Python graph library): rejected, because it is not needed: SQLite serves a 12-row walk from its indexes, and the repo is standard library only. A library would add a dependency and an hourly load step; the data is small enough to fit in memory, so it is the fallback if the query is measured too slow.
- recursive-sql (recursive queries on the SQLite export already read): chosen, because the required work is at most 12 indexed steps per request (above). The query, described and not applied: start from the submitter's solid manager (`kind = 'solid'` only, so dotted leads are never read); join `employee` for the grade; follow the manager's own solid line only while the current person's grade is below 7, so the first grade 7 or above is included as the last approver and nothing past them; carry the ids seen so far (a path column) and stop, flagging the claim for HR ops, when the next manager is already in it or is the submitter. A path column is safe here because each person has one solid line, so there is one route and no multiplication of rows. A plain Python loop of up to 12 indexed lookups would also work, but a single recursive statement avoids a query per level. How long it takes has not been measured (no database copy).
- no-graph (plain joins, no traversal): rejected, because the chain follows employee-to-manager links to a depth that depends on the data (up to 12), which is a walk and not a join across a link table.

## What would change the decision

- A measured p95 of the recursive query on a real export above the approval page's latency budget (the HR app or the page owner sets it; none is stated) would move this to in-process-library, since 6,400 people load in memory trivially each hour.
- The rules changing so that dotted lines can sign, or so that approval depends on amount and not only grade (hr/approvals.py `can_approve_amount` exists but is not part of the chain rule given), would change the query, and a second line per person would mean the path column should be replaced by deduplication on person; neither moves it to another option by itself.
- Org-wide analysis (for example span of control or every person's chain at once) as a batch job would favour in-process-library; the headcount or request rate growing by several orders of magnitude, with SQLite measured failing, would reopen graph-database.
