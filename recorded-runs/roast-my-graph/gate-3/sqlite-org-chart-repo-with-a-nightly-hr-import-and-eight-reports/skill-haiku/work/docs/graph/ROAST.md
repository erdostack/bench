# Roast: orgchart (schema.sql, import_hr.py, reports/)

Verdict: Not sound. One critical: last night's import put two people in a manager loop, which takes 54 employees out of the tree and makes the "Reports to" strip on their profiles, and the headcount report for the two managers, run forever. Fix the data with HR and make the import refuse a bad tree before go-live.

Judged against:
- Engine: SQLite, `hr.db` (README). Version: not stated.
- Size: about 3,000 people (README; `data/hr_export.csv` has 3,000 rows).
- Invariant: "The org is a tree: everyone has exactly one manager except the CEO, whose manager_id is empty" (README).
- Main path: `reports/chain_of_command.sql` is the "Reports to" strip on every profile (README, file comment).
- Nightly write: `python3 import_hr.py data/hr_export.csv` upserts the export and removes leavers (README, `import_hr.py`).
- Dashboards: the other reports feed the team and HR dashboards (README).

## Findings

### critical: `manager_id`
Two people manage each other, and the recursive queries have no way out.
Problem: `hr.db` has E2210 (Dev Abara) and E2391 (Hana Fischer) each naming the other as manager. 54 employees, including both, never reach the CEO. `reports/chain_of_command.sql` uses `WITH RECURSIVE` with `UNION ALL` and no depth bound, so the "Reports to" strip for those 54 never returns. `reports/headcount_under.sql` has the same unbounded recursion. A read-only test of the chain query for E2210 was still running when stopped. `schema.sql` only rejects a self-loop (`manager_id <> id`), which is not enough for a tree.
Fix: Reassign one of the two managers with HR. In `import_hr.py`, check inside the transaction, after the upserts and before the commit, that every employee reaches the one row with a NULL manager_id, and raise so the import rolls back if not. As a stopgap only, add `WHERE c.level < 50` to both recursive queries. That stops them hanging but leaves the data wrong.

### high: `open_role`
Leavers are deleted without checking open roles, and the report drops the role silently.
Problem: `import_hr.py` runs `DELETE FROM employee` and never sets `PRAGMA foreign_keys = ON`, so the reference from `open_role.manager_id` is not enforced. A leaver who is the hiring manager of an open role leaves a dangling reference, and `reports/open_roles.sql` (inner JOIN to employee) drops that role without an error. The stale step (`UPDATE employee SET manager_id = NULL`) also turns a report under a leaver into a second root, which breaks the README's rule with no error. Current `hr.db` has no dangling references, so this needs a leaver with an open role.
Fix: Set `PRAGMA foreign_keys = ON` on the import connection, so the delete fails and rolls back. Reassign the open role before removing the leaver. Replace the silent NULL update with a check that fails the import.

### low: `reports/tenure.sql`
Problem: The comment says "Median-ish tenure", but the statement computes `avg()` and truncates it with `CAST`, so the label and the number disagree.
Fix: Fix the comment to say mean, or compute a median with a window function if the page needs one.

### low: `emp_tmp_idx`
Problem: The index on `employee (manager_id)` that the direct-reports, span-of-control and headcount reports depend on has a name that says temporary.
Fix: Rename it in one transaction: `DROP INDEX emp_tmp_idx; CREATE INDEX employee_manager ON employee(manager_id);`.

## Holds up
- `employee_hired` on `employee (hired_on)`: `reports/new_joiners.sql` filters on a range of ISO date strings, which a text index serves. Would change if the date were stored in another format.
- `emp_tmp_idx` on `employee (manager_id)` (the index itself, not its name): `reports/direct_reports.sql` and `reports/span_of_control.sql` lead with that column. Keep the index whatever it is called.
- `open_role_manager` on `open_role (manager_id)`: serves the lookup from the hiring manager's side.
- `reports/by_location.sql`: groups on `location.code`, the primary key, so selecting `l.city` is valid, and the LEFT JOIN keeps empty locations.
- `reports/direct_reports.sql`: a single indexed equality with a sort on `name`, which is small per manager.

## Not checked
- The recursive queries were not run to completion; the test on `chain_of_command.sql` was stopped by a step cap, which shows it did not finish but does not give a time.
- SQLite version not stated; the test ran on the local SQLite, and the fixes assume plain SQL that has been valid for years.
- Whether the HR export itself can produce a leaver's report, and the data beyond these 3,000 rows, are outside the repo.
- Whether `INSERT OR IGNORE` on `location` could keep an outdated city was not checked (no conflicting rows in the export).

Roasted with erdostack: npx skills add usergraphtheory/erdostack
