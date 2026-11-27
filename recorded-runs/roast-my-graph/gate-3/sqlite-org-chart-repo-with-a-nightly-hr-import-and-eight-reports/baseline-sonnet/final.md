Roast of orgchart (schema.sql, import_hr.py, reports/). Full list in findings.json in the repo root (10 items).

The worst one is already in last night's hr.db. Two people manage each other: E2210 (Dev Abara) reports to E2391 (Hana Fischer), and E2391 reports to E2210. 52 more people sit below them, so 54 people never reach the CEO. `reports/chain_of_command.sql` uses `UNION ALL` with no depth limit, so the "Reports to" strip on each of those 54 profiles recurses forever and never returns. `reports/headcount_under.sql` has the same problem for those two managers. The schema's CHECK only stops someone managing themselves. Fix the manager in the HR system, add a depth cap (`WHERE c.level < 50`) to the chain query, and switch `headcount_under.sql` to `UNION`.

Next:

1. `import_hr.py` validates nothing. An empty or truncated export marks everyone as a leaver and deletes all of them in one committed transaction. It also accepted the cycle above. Add pre-commit checks: a row count floor, exactly one CEO, every manager present, no cycles, valid dates.
2. Leavers' reports are set to a NULL manager, which means "CEO", so you can end up with extra roots. The importer doesn't enable foreign keys, so a leaver's open role is left dangling and `open_roles.sql` drops it silently.
3. The upsert never updates `hired_on`, so a corrected hire date or a rehire is never applied. Locations are insert-or-ignore, so a city rename is never applied either.
4. `new_joiners.sql` has no upper bound, so it lists 18 people who start in the future. `tenure.sql` is labelled "median-ish" but is an integer-truncated average, and it also includes those future hires (negative tenure).
5. The README's "exactly one manager, tree" rules are not enforced by the schema. Add a one-root unique index and a date format CHECK.
6. Minor: `emp_tmp_idx` is the index every manager query depends on and its name invites someone to delete it. `hr.db` and the CSV (names, titles, hire dates for about 3,000 people) are checked in beside the code.

`by_location.sql`, `span_of_control.sql` and `direct_reports.sql` look fine. I read the files and queried hr.db read-only; I did not modify any data.
