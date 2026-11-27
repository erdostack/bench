# Graph decision

Decision: recursive-sql

Expense and leave sign-off must go up the solid reporting chain from the submitter's manager to the first grade 7 or above, stopping early at a loop; Jonas proposes Neo4j for it. The answer is a recursive query on the SQLite directory export the service already reads: each employee has at most one solid manager, so the chain is a single path of at most 12 steps, and a measured walk takes a fraction of a millisecond. The finding it turns on: the solid-line table is a functional graph, so the loops and the depth cap are handled by the query, not by a graph store.

## Workload facts

- Employees: 6,400 (stated by the user).
- Reporting lines: 7,900 (stated by the user), of which about 1,500 are dotted (stated by the user). Solid lines: 7,900 − 1,500 = 6,400 (derived from the two stated counts). With 6,400 employees and at most one solid line per employee, every employee except perhaps the top of the organisation has exactly one solid manager. The counts cannot tell whether the top person has a solid line.
- Solid-line uniqueness: enforced by the unique partial index `reporting_line_one_solid ON reporting_line(employee_id) WHERE kind = 'solid'` (`db/schema.sql`). Each employee therefore has one route upward, so a recursive walk returns one row per level, not one per route.
- Index on the manager side: `reporting_line_manager` on `reporting_line(manager_id)` (`db/schema.sql`).
- Depth: at most 12 levels (stated by the user). The walk stops at the first grade 7 or above (stated by the user), and never passes a dotted line (stated by the user).
- Loops: 23 cases where people end up as each other's line manager, from a half-applied March re-org (stated by the user; Lena found them). The rule: when the chain returns to someone already in it, including the submitter, it stops there and HR ops takes the claim by hand (stated by the user). The schema does not prevent loops (`db/schema.sql` allows any solid pair).
- Export size: about 3 MB SQLite file (stated by the user), refreshed hourly (`README.md`). Not in the repo (`.gitignore`).
- Load: the approval page opens about 200 times a day (stated by the user) = 200 / 86,400 = 0.0023 opens a second on average.
- What runs today: `hr/approvals.py` has `employee()` and `reporting_lines()`, which read one employee's direct lines; the chain is the TODO and is not implemented. `can_approve_amount` is unrelated to the walk.
- Measured, correctness and loops: a synthetic directory of 6,400 employees, 7,899 reporting lines (6,399 solid, 1,500 dotted), 23 mutual solid pairs and grades drawn from 1 to 9 (SQLite 3.53.1, Python 3.13). The recursive query, which carries the path as a string, stops at grade 7 or above, stops before any manager already in the path, and caps depth at 12, matched an independent Python walk for all 6,400 submitters. The query plan shows `SEARCH rl USING INDEX reporting_line_one_solid (employee_id=?)` inside the recursive step. The synthetic is not the HR export and was used for correctness and timing only (scratch run in this task, command not kept).
- Measured, timing: per submitter, median 0.014 ms, p99 0.045 ms, maximum 4.4 ms; synthetic chain length median 4, maximum 11.
- Arithmetic: at most 12 rows per walk, one walk per open of the page, 0.0023 walks a second on average. The database work is negligible.
- unknown: how many employees have no solid line (the top of the organisation; the export count does not say); whether the 12-level cap counts approvers or reporting lines; whether a loop-stopped chain should list the last person before the loop (the reading used here: the loop-back person is not listed and the claim is flagged); how many of the 23 loops are two-person pairs and how many are longer cycles; the page's latency budget (not stated); peak open rate. Looked in: `README.md`, `db/schema.sql`, `hr/approvals.py`, `hr/messages.py`, `hr/__init__.py`, `.gitignore`. The export file was not present.

## Options considered

- graph-database (a dedicated graph store, as Jonas proposes; no product named in the request): rejected, because the chain is a single path of at most 12 steps over one solid manager per employee, the whole table is 7,900 lines, and the measured walk is under a millisecond. Adopting one would add a second system kept in step with an hourly export for a load of about 0.0023 walks a second.
- in-process-library (the edges loaded into memory): not chosen. It would fit (the directory is about 3 MB), but it adds a loader and an hourly reload in every process; the recursive query on the existing file already meets the need.
- recursive-sql (recursive queries on the database already run): chosen, because the walk starts from one employee, SQLite is already the store, the partial unique index on solid lines and the manager index serve the walk, and the path string stops the loops. The query still needs one addition before it is used: it should report whether the chain ended at a grade 7 approver, at a loop, at a missing line or at the depth cap, so that HR ops can see which claims go to them. That is a remedy to test on the real export, not a measured result.
- no-graph (plain joins, no traversal): rejected, because the chain length depends on the data and runs up to 12 levels; one join does not reach it.

## What would change the decision

- The p99 time of the chain query on the real export, measured with the loop guard and the grade stop in place, exceeding the approval page's latency budget (the budget is not stated in the repo; the owner of the page sets it) would move this to in-process-library, with the chain precomputed after each hourly import.
- Chains that must cross more than the single directory export, or depth requirements above the 12 stated, changing the walk from bounded to unbounded and online at many times today's rate, would move this to graph-database; the sign-off policy owner sets that limit.
- A change to the Finance rule (for example, allowing dotted leads to sign) changes the query, not the choice; it is not a condition to move options.
