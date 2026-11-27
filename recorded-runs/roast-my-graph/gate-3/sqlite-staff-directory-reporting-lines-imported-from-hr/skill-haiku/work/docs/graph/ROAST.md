# Roast: staff directory (db/, import/)

Verdict: Not sound. The "Everyone under me" panel returns the right people but is slow for managers high in the tree. In a test on the copy, the panel for a manager with 3,994 people under them took 82 seconds on the data as stored. The cause is `manager_email`, which the importer stores in mixed case, so the queries have to `lower()` it and the index on it cannot be used. `direct_reports.sql` misses 24,150 reporting lines because of the same mixed case. Both are fixed by lowercasing on import and joining on the stored value.

Judged against:
- Engine: SQLite 3.53.1 (run here). The repo does not state a version.
- Size: about 60,000 employees, up to nine levels of management (README.md). directory.db has 60,000 employee rows (counted from the file), one with no manager.
- Interactive paths: the "Everyone under me" panel (db/queries/org_below.sql), profile chains (db/queries/managers_above.sql), and direct reports (db/queries/direct_reports.sql). README.md names the first two. The frequency of each is not stated.
- Batch path: import/import.py, rebuilt nightly from HR's CSV (README.md).
- Stated rule: addresses are case-insensitive for mail, and the directory treats them that way. The same manager can appear in two cases because HR keeps the address as typed (README.md).
- Stated invariant: `email` is unique and non-null (db/schema.sql).

## Findings

### critical: `manager_email`
The importer lowercases the employee's address and leaves the manager's as typed, so one column holds two spellings of the same address.
Problem: import/import.py stores `row["email"].strip().lower()` but `row["manager_email"].strip() or None`, with no lowercase. In directory.db, 24,150 of the 60,000 rows have an uppercase character in `manager_email`, and none of those values exactly matches an `email`. Two things break.
- `direct_reports.sql` runs `WHERE manager_email = :email` with no lowercase. For a manager with 46 reports on the lowercased count, it returns 30. Across all managers it misses 24,150 reporting lines.
- `org_below.sql` joins `lower(e.manager_email) = lower(b.email)`. That expression cannot use the `employee_manager` index, so the plan scans `employee` for each person it reaches. Measured on the copy: 82 seconds for a 3,994-row panel as stored, and 49 seconds after lowercasing the data in memory, because the query still calls `lower()`. With the join on `e.manager_email = b.email`, the same panel took 0.03 seconds. The top of the tree (59,999 rows) took 0.28 seconds in the same test. The current query on that panel was not run; by extrapolation from the 3,994-row run it would take about 12 minutes, so treat that as an estimate.
Fix: In import/import.py, store `row["manager_email"].strip().lower() or None`. Migrate the existing rows with `UPDATE employee SET manager_email = lower(manager_email);` (a single-column change, so the unique key on `email` is not affected). In db/queries/org_below.sql, change the join to `ON e.manager_email = b.email`. In db/queries/direct_reports.sql, compare with `lower(:email)`. Check the plans again: the step should read `SEARCH e USING INDEX employee_manager (manager_email=?)`.

### low: `load`
Problem: import/import.py runs `executescript` on `db_path` with `CREATE TABLE employee`, with no check for an existing file. A second run against the same file fails. If the nightly job rebuilds in place, the intranet can read a half-loaded file while the import runs. The job's steps are not in this repo, so this is a question to confirm.
Fix: Write the import to a temporary file in the same folder, then rename it over the live file once the load commits. The rename is atomic, so readers see either last night's data or tonight's.

## Holds up
- `managers_above.sql`: the first step reads `email = lower(:email)`, which the UNIQUE index serves. The recursion joins `e.email = lower(a.manager_email)`, which also uses that index. Because it lowercases the manager side, it is correct on the mixed data as stored. It stops on a loop, since the UNION carries (email, manager_email) and each employee has one manager, so the rows form a finite set.
- `org_below.sql` termination: the recursion uses `UNION` on the email alone, so it stops even if the HR data contains a manager loop. The final `b.email <> lower(:email)` keeps the person from appearing under themselves.
- `schema.sql`: `email` is unique and non-null, and `employee_manager` on `manager_email` serves the direct-reports lookup, which the plan confirms (`SEARCH employee USING INDEX employee_manager (manager_email=?)`). Once the stored value is lowercase, the same index serves the panel.
- The import is loud on bad data: two HR rows whose emails differ only in case violate the unique key, and the `with con:` block rolls back the whole load instead of loading part of it.

## Not checked
- The intranet code is not in this repo, so it is not known which of the three queries the pages call, or how often.
- The rebuild procedure (whether the old file is removed first, and where the live copy is) is not in the repo.
- The root-panel timing for the current query was not run; the estimate above is extrapolated.
- directory.db was read through a read-only connection. The fixes were tested on an in-memory copy with the manager column lowercased, and the import was not run.
