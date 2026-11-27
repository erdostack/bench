# Graph decision

Decision: recursive-sql

Bram wants the customer organisation hierarchy moved into a graph database before it gets out of hand, but the two numbers agreed with ops for reopening the storage question are both well inside their limits: the nightly rollup takes about 2 minutes against a 20-minute trigger, and the account-page subtree query is 12 ms p95 against a 150 ms trigger. The traversals already run as recursive SQL on indexed tables, so the decision is to change nothing; the finding it turns on is the 10-fold headroom on the rollup, with the invoice volume the one unknown that could erode it.

## Workload facts

- Organisations: 2,300 (stated by the user).
- Deepest group: 7 levels (stated by the user).
- Nightly rollup: about 2 minutes (stated by the user); trigger to revisit storage: over 20 minutes, which must fit a 30-minute batch window (stated by the user). Headroom: 20 / 2 = 10 times.
- Account-page subtree query: 12 ms p95 (stated by the user); trigger: over 150 ms p95 (stated by the user, agreed with ops). Headroom: 150 / 12 = 12.5 times.
- Load: about 40 page loads a minute (stated by the user) = 0.67 subtree queries a second at peak as stated; the rollup runs once a night.
- Traversals in the repo: `accounts/subtree.py` walks down from one organisation through `org.parent_id` with a depth cap of 30 (`SUBTREE_SQL`); `rollups/rollup.py` walks up from every organisation to its ancestors with the same cap, then sums invoices per ancestor (`ROLLUP_SQL`). Both are recursive SQL over the SQLite file `var/orgbook.db` (`README.md`, not in the repo).
- Indexes in place: `org_parent` on `org(parent_id)` serves the downward walk (`db/schema.sql`); the primary key on `org(id)` serves the upward join; `invoice_org` on `invoice(org_id, issued_on)` serves the rollup's per-organisation invoice lookup (`db/schema.sql`). The subtree query's plan shows `SEARCH o USING INDEX org_parent (parent_id=?)` (measured, below).
- Walk shape: each organisation has one parent (`parent_id`), so an upward walk has one route per organisation; the rollup's ancestor rows equal the sum of (depth + 1) over all organisations, with no multiplication from routes. The CRM is said to forbid loops (comment in `accounts/subtree.py`); this is not verified in the repo.
- Measured, synthetic tree of 2,300 organisations, max depth 7 levels, SQLite 3.53.1 under Python 3.13 (scratch run in this task, command not kept; not the CRM data): subtree query, 200 random roots, median 0.008 ms, p95 0.028 ms, maximum 12 ms; rollup, 200,000 synthetic invoices, 3.8 s, with 13,972 ancestor rows (sum of depth + 1 over the synthetic tree). The synthetic subtree query is much faster than the stated 12 ms p95, which the production hardware or the real tree may explain; the synthetic is used for the shape of the cost, not for the production number.
- Scaling of the rollup: its cost is invoice rows times the depth each invoice is joined through, so total work is the sum over invoices of (number of ancestors + 1). The invoice count is not in the repo. At the stated 2 minutes, the invoice volume the production run is handling is unknown.
- Arithmetic: the rollup's two-minute figure is 10 times below the 20-minute trigger; a 10-fold rise in invoice rows at the same depth would bring it to about 20 minutes if the time grows linearly (an extrapolation from one synthetic run, not measured).
- Freshness: the rollup is nightly and the CRM load is evening (`README.md`); no freshness requirement is stated beyond the batch window.
- unknown: the invoice row count and its growth; the production hardware and SQLite version; the real depth distribution of the 2,300 organisations (the synthetic was random); whether the CRM can produce loops (not checked); whether the 12 ms and 2-minute figures are from a single run or from logged percentiles; the merger's expected growth in organisations and invoices (not stated). Looked in: `README.md`, `db/schema.sql`, `accounts/subtree.py`, `rollups/rollup.py`, `.gitignore`. The database file was not present.

## Options considered

- graph-database (a dedicated graph store, as Bram proposes): rejected, because both measured paths are within their agreed limits (rollup 2 min against 20; subtree 12 ms p95 against 150), the walks are one parent per organisation over 2,300 rows, and the page load is under one query a second. Adopting one would add a second system, a sync from the nightly CRM load, and a new query language, with no stated requirement it meets.
- in-process-library (the edges loaded into memory): rejected, because the hierarchy is 2,300 parent links, which would fit trivially, but the rollup is driven by the invoice table, which a graph library does not remove; a reload would add a loader and a copy per web process for no gain.
- recursive-sql (recursive queries on the database already run): chosen, because the walks start from one organisation or run once a night, the indexes match the walk, the stated timings are inside the limits agreed with ops, and the database is already operated. No change is needed now.
- no-graph (plain joins, no traversal): rejected, because the subtree and the ancestor sums are walks of data-dependent depth up to 7 levels; a fixed join does not reach them.

## What would change the decision

- The nightly rollup exceeding 20 minutes, measured on the production run (the trigger agreed with ops), would reopen the storage question; the first step would be a rollup that sums invoices once per organisation and then rolls the sums up the tree, which removes the repeated invoice join and is a remedy to run and measure, not a result here.
- The account-page subtree query exceeding 150 ms p95 over the same window the team already logs would reopen the question, with the same first step of checking the plan and index use before any new store.
- Organisations or invoices growing by a factor that brings the rollup near 20 minutes at the current trend, with the trend from the nightly logs (the owner of those logs is ops).
- A requirement for a different traversal (for example, paths between two arbitrary organisations across groups at online latency) would be a new question; it is not a condition to move options under the current workload.
