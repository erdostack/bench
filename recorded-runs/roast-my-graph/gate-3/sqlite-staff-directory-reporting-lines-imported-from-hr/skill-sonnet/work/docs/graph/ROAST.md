# Roast: staff directory (db/schema.sql, db/queries/, import/import.py, against directory.db)

Verdict: The "everyone under me" panel is slow because of one stored value, not because SQLite is slow: the nightly import lowercases `email` but stores `manager_email` exactly as HR typed it (24,150 of 60,000 rows are not lowercase in last night's copy), so `org_below.sql` has to wrap both sides of its join in `lower()`, which keeps the `employee_manager` index out of the recursion. On the 60,000-person copy it does not finish in 60 seconds for the top three managers (the whole company, a 14,217-person org, a 7,580-person org) and takes 16 seconds for an 881-person org. Lowercase `manager_email` at import, drop the `lower()` calls, and the same panel for the whole company runs in about half a second (run on a copy). Two criticals from the same cause, and one high.

Judged against:
- Engine: SQLite, rebuilt every night from HR's CSV export, read by the intranet (README.md). SQLite version here: 3.53.1 (run); version in production: not stated.
- Size: 60 thousand employees, up to nine levels of management (README.md). `directory.db` has 60,000 rows, depth up to 8 managers above a person, no cycles, one person without a manager (the top).
- Stated rule: addresses typed by HR can differ in case (`R.Okafor@corp.example` and `r.okafor@corp.example`) and "the directory treats them that way", i.e. as the same address (README.md).
- Reads: profile pages show the chain of managers (`managers_above.sql`) and the "Everyone under me" panel (`org_below.sql`), the panel people complain about (user request, README.md). How often they run, and whether `direct_reports.sql` is wired to a page: not stated.
- Writer: `import/import.py`, nightly, one transaction, the only writer found.

## Findings

### critical: `manager_email`
Lowercased the employee, forgot the boss. Two fifths of the company's reporting lines are in costume, and every query has to unmask them one `lower()` at a time.
Problem: When the nightly `load` in import/import.py inserts rows, it stores `email` as `.strip().lower()` but `manager_email` as `.strip() or None`, so `manager_email` keeps HR's case: 24,150 of 60,000 rows in `directory.db` have a `manager_email` that is not lowercase (for one manager the 46 direct reports carry three spellings, 30 / 9 / 7), and none is missing once lowercased. Everything that joins `manager_email` to `email` then either gets wrong results (`direct_reports.sql`) or cannot use `employee_manager` (`org_below.sql`).
Fix: Store it the way `email` is stored: in `load`, change the last parameter to `row["manager_email"].strip().lower() or None`. The directory is rebuilt every night, so the next load fixes the data; to fix it before then run `UPDATE employee SET manager_email = lower(manager_email) WHERE manager_email <> lower(manager_email);` (tried on a copy: 24,150 rows changed, no manager missing). Afterwards `employee_manager` can serve the join. Optional insurance: `CHECK (manager_email IS NULL OR manager_email = lower(manager_email))` on the column in db/schema.sql so the next writer cannot reintroduce it. Assumes SQLite 3.53 behaviour as run here; nothing version-specific is used.

### critical: `org_below.sql`
The panel asks for "everyone under me" and answers with "please hold" for the whole afternoon. A recursive query that does a full scan per level and lowercases 60,000 addresses while it thinks about it.
Problem: When a manager opens "Everyone under me", the recursive step `JOIN below b ON lower(e.manager_email) = lower(b.email)` cannot use the index `employee_manager`, because `manager_email` is wrapped in `lower()`; the plan shows `SCAN e` inside the recursive step and an automatic index built on the fly. Run read-only on a copy of `directory.db`: the top manager (59,999 below), a 14,217-person org and a 7,580-person org were all still running after 60 seconds, an 881-person org took 16.3 s and a 59-person org 0.7 s. On the stated 60,000 people and nine levels, the panel cannot finish for any senior manager.
Fix: After normalising `manager_email` (see `manager_email`), compare the columns directly so the index is used:
```
WITH RECURSIVE below(email) AS (
    SELECT lower(:email)
    UNION
    SELECT e.email
    FROM employee e JOIN below b ON e.manager_email = b.email
)
SELECT e.name, e.title, e.email
FROM below b JOIN employee e ON e.email = b.email
WHERE b.email <> lower(:email)
ORDER BY e.name;
```
Run on a copy with `manager_email` lowercased: plan is `SEARCH e USING INDEX employee_manager (manager_email=?)` and `SEARCH ... sqlite_autoindex_employee_1 (email=?)`; whole company (59,999) 0.55 s, 14,217 in 0.09 s, 7,580 in 0.05 s, 881 in 0.006 s, and the same result counts as before. Stopgap that does not need a data change: `COLLATE NOCASE` on `manager_email` and its index; but the data fix is simpler and matches how `email` is stored. An index on `lower(manager_email)` would also work but keeps the mixed-case data.

### high: `direct_reports.sql`
It is the only query that does not lowercase anything, which is how it ends up counting 30 of someone's 46 reports.
Problem: `WHERE manager_email = :email` is an exact, case-sensitive comparison against a column that keeps HR's case, so for a manager whose reports are stored under three spellings of the address it returns only the ones spelled like the argument. Run on `directory.db` for `chen.moreau1350@corp.example`: 46 people report to them (case-insensitive), the query returns 30. With 24,150 rows affected, the README rule that addresses are case-insensitive is broken for direct reports across the company. (Whether a page calls this query is not stated in the files.)
Fix: Same cause as `manager_email`: once the column is lowercased, compare with `WHERE manager_email = lower(:email)` so a mixed-case argument still matches. Tested on the normalised copy: 46 rows. Stopgap before the data change: `WHERE lower(manager_email) = lower(:email)` (correct, but a scan of 60,000 rows per call).

## Holds up
- `managers_above.sql`: joins `e.email = lower(a.manager_email)`, which looks like the same mistake but is not: the lowercasing is on the stored `manager_email` side being looked up in the `email` column, which is stored lowercase and unique (`UNIQUE` on `email` gives the index), so each step is an index search and the result is correct for mixed-case `manager_email`. At most nine steps. It keeps working after the data fix; the `lower(a.manager_email)` can then be dropped as tidying (low, optional).
- `employee_manager`: the index is right for the recursion and for `direct_reports.sql`; it is unused today only because of `manager_email`'s case and the `lower()` calls. Do not add a second index.
- Recursion guard: `org_below.sql` and `managers_above.sql` use `UNION` over the email alone, so a reporting loop in the HR export could not make either run forever, and `directory.db` has no loop. Safe as written.
- `employee` as one table with `manager_email` pointing at another row: one row per person and the manager is a property of the person; there is no node or table between two others and no packed list. Right for a tree of this size. (No foreign key from `manager_email` to `email`: all 60,000 managers resolve in the copy, and an export with a dangling manager is a what-if nobody stated.)
- `load`: one transaction, so a failed load rolls back instead of leaving half a directory.

## Not checked
- Production: only the nightly copy `directory.db` was read, on a copy in a temporary file. Production's SQLite version and the real export's content are not known.
- `import.py` was read, not run against a real HR CSV; how `db_path` is created each night (a fresh file, since `schema.sql` has no `IF NOT EXISTS`) is not shown.
- How often the panel is opened and which page uses `direct_reports.sql`: not stated.
- Timing is from this machine and shows plan shape and correctness; the 60-second cut-off means the large orgs' true time is longer, not that it is exactly 60 s.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
