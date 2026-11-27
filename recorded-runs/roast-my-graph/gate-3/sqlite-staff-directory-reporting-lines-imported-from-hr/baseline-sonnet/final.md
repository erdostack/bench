The "everyone under me" panel is slow because of one function call in `db/queries/org_below.sql`, and there is a data bug underneath it that also breaks the direct reports list.

**Why it is slow.** The recursive step joins on `lower(e.manager_email) = lower(b.email)`. Calling `lower()` on the column stops SQLite using the `employee_manager` index, so every level of the recursion scans all 60,000 rows. I timed it on a copy of last night's `directory.db`:

- A manager with 30 people below them: 0.6 s.
- 299 people below: 5.6 s.
- 2,859 people below: 56 s.
- The CEO (59,999 people below): over two minutes, and I stopped it.

**The root cause.** The README says addresses are case-insensitive, but `import/import.py` lower-cases `email` and only strips `manager_email`. In the copy, 24,150 of 60,000 rows have a `manager_email` whose case differs from the manager's stored address. One manager appears as `CHEN.MOREAU1350@CORP.EXAMPLE`, `Chen.Moreau1350@Corp.Example` and `chen.moreau1350@corp.example`. The `lower()` calls in the queries are a workaround for that.

**The same bug makes `direct_reports.sql` wrong.** It uses a plain `manager_email = :email`, so it only returns reports whose spelling matches. For that manager it returns 30 of their 46 direct reports, with no error.

**Fix.**
1. Store `lower(trim(manager_email))` in `import/import.py`.
2. Change `org_below.sql` to join on `e.manager_email = b.email`.
3. Add a `CHECK (manager_email = lower(manager_email))` so it cannot drift again.

I tried steps 1 and 2 on a throwaway copy. The plan switches to `SEARCH e USING INDEX employee_manager`, and the CEO query finishes in 0.83 s and returns all 59,999 people. I did not change any files in the repo.

Smaller findings:

- The nightly load is not idempotent: the schema script fails if the database file exists, and loading into the live file lets the intranet see a half-loaded directory.
- There are no loader checks for missing managers, cycles or duplicate emails.
- There is no foreign key on `manager_email`.
- `managers_above.sql` and `org_below.sql` return no level or order, so the profile page cannot show the hierarchy.

`findings.json` in the repo root has 8 entries with element, severity, problem and fix, ready to paste into the tracker.
