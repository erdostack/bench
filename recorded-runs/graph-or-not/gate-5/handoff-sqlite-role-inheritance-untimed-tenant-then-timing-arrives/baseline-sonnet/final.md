Decision: recursive-sql

Stay on the existing SQLite database and keep traversing with the recursive query. I didn't change any code.

What it rests on:
- **Your measurement:** p95 of 1.8 s over 500 runs, with indexes in place, on the real enterprise tenant. That is a number from the current approach. No other option has been measured.
- **The problem fits SQL:** the report is reachability over `role_inherits` (every role a user holds, directly or inherited), joined to permissions. The data is already in the database, and the query already works.
- **The query has slack:** `EFFECTIVE_SQL` carries a comma-separated path string on every row to avoid cycles. That means it re-walks a role once for every route that reaches it, so the cost grows with the number of routes rather than the number of roles. On a synthetic test (8 layers of 4 roles, every role inheriting all roles in the next layer), swapping it for a plain `UNION` recursion gave identical results about 10x faster. `UNION` removes duplicate rows, so cycles still terminate. The enterprise tenant's real shape may differ, so treat 10x as an indication, not a prediction.
- **A graph database or in-process library wouldn't be the next step even if 1.8 s is too slow.** Either would add a second store to keep in sync, or a cache to invalidate on every `grant`/`revoke`. That is only worth it after the cheap SQL fix has failed.

What I don't know: whether 1.8 s is acceptable. I found no latency target anywhere in the repo, and I don't know whether this runs on every page load or only occasionally. If it's too slow, the next step is the `UNION` rewrite, checked against Jun's tenant data. A target would also tell us when to revisit this.

I added a "Decision" section to `README.md`, the only place the repo documents anything. It records the decision, the evidence, the reasoning and when to revisit. No decision record existed before.
