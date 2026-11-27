Decision: recursive-sql

Jun's timing settles it. Under Sanne's rule the indexed recursive query on SQLite stays while it meets the 3 s p95 budget. On the enterprise tenant it measures 1.8 s p95 over 500 runs, so it meets the budget with 1.2 s of headroom, about 60% of the limit. That means no move to the identity team's graph store and no in-process library. Change nothing in `authz/effective.py`.

I updated `docs/graph/DECISION.md`. The decision changes from need-more-information to recursive-sql. The new timing is recorded next to the old "unmeasured" state, and the options and the "what would change it" list are updated. That file is the only thing I changed. I didn't run anything myself, because there's no database or timing output in the repo. The 1.8 s is your figure, recorded as stated by you.

Things I could not confirm:
- The worst case on the enterprise tenant.
- Which users the 500 runs sampled. Ideally they include the users with the most and deepest roles.
- Whether the test box matches production.

What would reopen it:
- A p95 over 3 s on the enterprise tenant, for example after it grows. That would send the work to the graph store under Sanne's rule.
- The report becoming user-facing, or its rate rising far above about 200 runs a day.
- Inheritance growing in a diamond shape. The query returns one row per route, not per distinct role, so route count is what would use up the 1.2 s of headroom.
