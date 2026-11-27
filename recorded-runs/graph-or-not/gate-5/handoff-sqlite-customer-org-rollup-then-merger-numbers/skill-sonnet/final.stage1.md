Decision: recursive-sql

A graph database is not worth it on the evidence we have. What you run today already meets the need, so the advice is to change nothing.

The numbers it turns on:
- The nightly rollup takes about 2 minutes against the 20-minute trigger you agreed with ops. That is 10 times headroom, inside a 30-minute window.
- The account-page subtree query is 12 ms p95 against the 150 ms trigger. That is 12.5 times headroom, at about 40 page loads a minute.
- `org.parent_id` is a single column, so the hierarchy is a forest of trees, and `org_parent` indexes the column the subtree walk enters by. A tree walk visits each organisation once, so `UNION ALL` does not multiply rows. The ancestor table in the rollup is at most about 2,300 x 8 = 18,400 rows.

A graph database would add a second stateful system, a feed from the CRM and a new query language, to fix something neither of your limits shows is broken. The merger is a reason to re-measure, not a reason to move.

What I could not do:
- There is no copy of `var/orgbook.db` in the repo, so I measured nothing myself. The timings are the ones you gave.
- Nobody has stated the post-merger number of organisations or invoices. If the merged data is expected to be many times 2,300 organisations, run both queries on a copy of the merged data before deciding anything.
- If either limit is passed (rollup over 20 minutes, or subtree over 150 ms p95), check the query plan first, because the time may be in the `invoice` join and not in the walk.

Nothing in the repo was changed apart from the new `docs/graph/DECISION.md`.
