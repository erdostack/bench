# Roast: orgchart (schema.sql, import_hr.py, reports/)

Verdict: Two of the three serious problems share one cause: last night's import loaded a reporting loop (E2210 and E2391 are each other's manager), and neither the import nor the schema notices. The "Reports to" strip on every profile hangs for the 54 people at or below that loop, and the headcount report hangs for the two managers in it. Fix the import first; the rest is tidy-up.

Judged against:
- Engine: SQLite, `hr.db` (README.md); version: not stated. Checked with SQLite 3.53.1 locally.
- Size: about 3,000 people (README.md); `hr.db` holds 3,000 employees, 5 locations and 40 open roles, identical to `data/hr_export.csv`.
- Batch: `import_hr.py` upserts the HR export every night (README.md).
- Invariant: "The org is a tree: everyone has exactly one manager except the CEO, whose `manager_id` is empty" (README.md).
- Interactive: `chain_of_command.sql` is the "Reports to" strip "shown on every profile"; the other reports feed the team and HR dashboards (README.md).

## Findings

### critical: `import_hr.py`
The README promises a tree. The importer promises to load whatever HR sends, trees, wreaths and Moebius strips included.
Problem: When `run` loads `data/hr_export.csv`, nothing checks the README's tree rule. The CHECK in `schema.sql` only stops a person managing themselves, so the export's loop `E2210 -> E2391 -> E2210` was imported as is (last night's `hr.db` has it). It also cuts those two and everyone below them off from the CEO: 54 people in total, so `headcount_under.sql` for `E1000` returns 2,945 instead of 2,999.
Fix: Before the transaction commits, inside `with con:`, fail the whole import if anyone is not reachable from the single root:
```python
roots = con.execute("SELECT count(*) FROM employee WHERE manager_id IS NULL").fetchone()[0]
lost = [i for (i,) in con.execute(
    "WITH RECURSIVE reach(id) AS (SELECT id FROM employee WHERE manager_id IS NULL "
    "UNION SELECT e.id FROM employee e JOIN reach r ON e.manager_id = r.id) "
    "SELECT id FROM employee WHERE id NOT IN (SELECT id FROM reach) ORDER BY id")]
if roots != 1 or lost:
    raise SystemExit(f"{roots} roots, {len(lost)} people not under the CEO, first: {lost[:1]}; nothing imported")
```
(`UNION` over ids only finishes on a loop; checked on the shipped data, it lists exactly the 54.) The raise rolls the import back, so tonight's leavers and joiners also wait until the source is fixed: the trade-off is deliberate. Migration: HR has to correct the manager of `E2210` or `E2391`; the files cannot say which is right.

### critical: `chain_of_command.sql`
Climb the org chart until you reach the CEO, or forever, whichever comes first. For 54 people, it picks forever.
Problem: When the profile strip runs for any of the 54 people at or below `E2210`/`E2391`, the recursion `UNION ALL` ... `JOIN chain c ON e.id = c.manager_id` walks the loop endlessly; the `level` counter makes every row new, so it never ends. I ran it with a work cap against `hr.db` for `E2210` and for a person below the loop: both were interrupted by the cap, while `E1043` returns its 2 managers.
Fix: Stopgap, since the loop is a data fault the import should reject: carry the path and refuse to revisit a row. Add `path` to the CTE: `chain(id, manager_id, level, path)`, anchor `SELECT id, manager_id, 0, ',' || id || ',' ...`, recursive member `SELECT e.id, e.manager_id, c.level + 1, c.path || e.id || ',' ... WHERE instr(c.path, ',' || e.id || ',') = 0`. Checked on `hr.db`: it now finishes for `E2210` (one manager, `E2391`) and returns the same rows as before for `E1043`.

### high: `headcount_under.sql`
Counts everyone below a manager, and for the two managers in the loop counts them with enthusiasm and no stopping condition.
Problem: When the report runs for `E2210` or `E2391`, each is below the other, so the `UNION ALL` recursion never ends (interrupted by a work cap when I ran it for `E2210`). It is fine for everyone else, including `E1000` (2,945). Narrower than the profile strip, so `high`.
Fix: Stopgap until the import rejects loops: change `UNION ALL` to `UNION`. The recursive rows carry only the id, so duplicates are dropped and the walk ends; on `hr.db` it returns 54 for `E2210` and still 2,945 for `E1000`.

### low: `emp_tmp_idx`
A temporary index, which has been sitting there being load-bearing since forever.
Problem: The name says "tmp" but it is the only index on `employee (manager_id)`: `direct_reports.sql` uses it (`SEARCH employee USING INDEX emp_tmp_idx`), and so do `headcount_under.sql` and `span_of_control.sql`. Dropping it because of its name would turn the recursion and team pages into scans. Every other index is named `<table>_<column>`.
Fix: Rename, do not drop: `DROP INDEX emp_tmp_idx; CREATE INDEX employee_manager ON employee (manager_id);` in one transaction, and the same name in `schema.sql`.

### low: `hired_on`
Everything about a person is refreshed nightly except the one date the tenure report is built on.
Problem: The `ON CONFLICT (id) DO UPDATE SET` in `import_hr.py` updates name, title, location and manager_id but not `hired_on`, so a corrected hire date in the export never reaches `hr.db`. Today the file and the database agree, so this is a question: is `hired_on` meant to be frozen at first import?
Fix: If not, add `hired_on = excluded.hired_on` to the `SET` list. If so, add a comment saying it is deliberate.

### low: `new_joiners.sql`
"New joiners" includes people who have not joined yet.
Problem: `hired_on >= date('now', '-30 days')` has no upper bound, and 18 of the 3,000 rows have a `hired_on` after today (up to 2026-12-27), so 18 of the 34 rows it returns are future starters. The files do not say whether pre-boarding people should show; confirm.
Fix: If not wanted, add `AND hired_on <= date('now')`.

### low: `tenure.sql`
The comment says "median-ish" and the query computes a mean, with 18 people who start next month counted as negative tenure.
Problem: `avg(julianday('now') - julianday(e.hired_on))` averages the same 18 future dates in, and the `CAST ... AS INTEGER` truncates rather than rounds. The comment and the arithmetic disagree; confirm which is meant.
Fix: Say "mean" in the comment, or compute a real median; exclude future `hired_on` if only started staff count.

## Holds up
- `emp_tmp_idx`, `employee_hired`, `open_role_manager`: every lookup in `reports/` has an index leading with its column (`manager_id`, `hired_on`, `open_role.manager_id`) or is a primary key search; `new_joiners.sql` is `SEARCH ... USING INDEX employee_hired`. `tenure.sql` and `by_location.sql` scan all 3,000 rows, which is fine for a dashboard at this size.
- `by_location.sql`: the `LEFT JOIN` keeps locations with nobody in them, and `count(e.id)` counts people, not rows.
- `span_of_control.sql`: counts direct reports per manager from one join; no duplicate rows.
- `direct_reports.sql`: index search, and the sort is over one manager's reports.
- `location` (code, city) kept apart from `employee`: three-thousand rows share five cities, so the city is stored once, and `by_location.sql` reads it.
- `INSERT OR IGNORE INTO location` and the upsert in `import_hr.py`: one transaction, idempotent, safe to rerun.

## Not checked
- Whether any `open_role.manager_id` can belong to someone who leaves: `import_hr.py` deletes leavers without enabling `PRAGMA foreign_keys`, so such a role would stay and drop out of `open_roles.sql` silently. No such row exists today (`PRAGMA foreign_key_check` is clean), so it is a question, not a finding.
- What happens when an export is empty or truncated: the stale-leaver step would delete everyone not in it.
- How the web app calls `chain_of_command.sql` (timeouts, retries) when it hangs.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
