The "Everyone under me" panel is slow because of one stored value, `manager_email`, not because SQLite is slow. `import.py` lowercases `email` but stores `manager_email` exactly as HR typed it. In last night's `directory.db`, 24,150 of 60,000 rows have a non-lowercase `manager_email`. To match them, `org_below.sql` wraps both sides of its join in `lower()`, and that stops SQLite from using the `employee_manager` index.

I ran the queries on a copy of `directory.db`, so the original is untouched. The panel for the top manager (59,999 people below), a 14,217-person org and a 7,580-person org was still running after 60 seconds. An 881-person org took 16 seconds. On the copy, I lowercased `manager_email` and dropped the `lower()` calls. The company-wide panel then returned the same 59,999 rows in about 0.55 seconds, and the 881-person org took 0.006 seconds.

Findings, worst first:
- **critical, `manager_email`:** lowercase it at import with `row["manager_email"].strip().lower() or None`. The nightly rebuild then fixes the data. To fix it sooner, run the one-line `UPDATE` given in the roast.
- **critical, `org_below.sql`:** compare the columns directly in the recursive join (`e.manager_email = b.email`) once the data is lowercase. The full query is in `docs/graph/ROAST.md`.
- **high, `direct_reports.sql`:** it matches case-sensitively, so it misses reports stored under another spelling. For `chen.moreau1350@corp.example` it returns 30 of their 46 reports. After the data fix, use `WHERE manager_email = lower(:email)`. I don't know whether a page calls this query.

`managers_above.sql` is fine. It looks up the lowercase, unique `email` column, so it is correct and uses the index. The `employee_manager` index is right too. Neither query can loop forever, and the data has no loops.

I only had last night's copy, not production. I didn't run `import.py` against a real HR file, and I don't know how often the panel is opened.

Files:
- docs/graph/ROAST.md
- findings.json
