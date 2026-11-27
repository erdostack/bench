The timeouts are caused by queries/acting_for.sql, and the cause is a cycle, not load.

What is wrong:
- The recursive CTE in queries/acting_for.sql uses UNION, but the row it deduplicates on includes handoffs, and handoffs goes up by one on every step. A cycle therefore never produces a repeated row, so the recursion never stops. The comment at the top of the file says UNION stops mutual delegations from looping, and that is wrong.
- Mutual delegations are common in the demo tenant: 121 pairs. Each pair is a two-person cycle. On approvals.db, 224 of 400 users have a query that never returns, because their chain reaches a cycle. The inbox runs this query on every page load, so those people see the timeouts. I interrupted the query for one affected user after 5 seconds to confirm this.

The fix:
- Add a depth limit to the recursive step: AND a.handoffs < (SELECT COUNT(*) FROM app_user). A shortest path can have at most n-1 hops, so the limit drops nothing, and UNION keeps the row count bounded.
- With that change, the query matched a breadth-first reference for all 400 users on approvals.db, and each run finishes almost at once.
- Correct the comment in the file, and consider caching the result per user for the page load.

Smaller items:
- schema.sql stores delegation.valid_until as TEXT with no format check, and both queries compare it as a string against date('now'). A badly formatted date would be compared wrongly without any error. All current rows are fine. Add a CHECK on the format.
- queries/team_rollup.sql relies on the CHECK on team.parent_id to stop its UNION ALL recursion. That is safe today, but the dependency is not written down. Switching to UNION and noting the dependency removes the risk.

Full list with element names is in findings.json in the repo root. I did not change any files other than writing findings.json. The database was opened read-only.
