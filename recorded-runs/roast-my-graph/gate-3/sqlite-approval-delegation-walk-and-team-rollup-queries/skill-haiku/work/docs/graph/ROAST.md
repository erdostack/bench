# Roast: approvals schema and queries (acting_for, inbox, team_rollup)

Verdict: Critical. `queries/acting_for.sql` never finishes for a user whose delegation chain reaches a mutual pair, and the inbox runs it on every page load. Its comment says `UNION` stops loops. It does not, because `handoffs` changes on every row, so no two rows are ever equal. The fix is inside that one query. The other two queries and the schema hold up.

Judged against:
- SQLite 3.53.1 (approvals.db has the same schema text as schema.sql)
- `queries/acting_for.sql`: "The approval inbox runs it on every page load" (README.md)
- Delegations "come in pairs inside a team", and chains are allowed (README.md). The demo tenant has 324 delegations among 400 people, and 121 mutual pairs in the data (approvals.db)
- Team tree depth is bounded by `CHECK (parent_id IS NULL OR parent_id < id)` in schema.sql
- The approval inbox is interactive; the team rollup is a monthly batch (README.md)

## Findings

### critical: `queries/acting_for.sql`
Problem: When Ana delegates to Ben and Ben to Ana (the schema allows this, its only check is `from_user <> to_user`), the recursive step `acting(user_id, handoffs)` produces (Ben, 2), then (Ana, 3), then (Ben, 4), and so on. Each row is new because `handoffs` differs, so `UNION` removes nothing and the walk never ends. In the demo tenant, 224 of 400 users reach a loop (checked by walking the delegation graph). Running the query for user 1, which is in a mutual pair, was interrupted after 5 seconds on a read-only copy.
Fix: Carry the visited path and stop any step that would revisit a user:
```sql
WITH RECURSIVE acting(user_id, handoffs, path) AS (
    SELECT from_user, 1, ',' || :user_id || ',' || from_user || ','
    FROM delegation
    WHERE to_user = :user_id AND valid_until >= date('now')
    UNION ALL
    SELECT d.from_user, a.handoffs + 1, a.path || d.from_user || ','
    FROM delegation d
    JOIN acting a ON d.to_user = a.user_id
    WHERE d.valid_until >= date('now')
      AND instr(a.path, ',' || d.from_user || ',') = 0
)
SELECT u.email, MIN(a.handoffs) AS handoffs
FROM acting a
JOIN app_user u ON u.id = a.user_id
WHERE a.user_id <> :user_id
GROUP BY u.email
ORDER BY handoffs, u.email;
```
This version was run on an in-memory copy of approvals.db for all 400 users. Every result matched a Python breadth-first search for the shortest hop count, and the slowest user took under a millisecond. The path guard enumerates simple paths, so its cost grows with how branched the delegation web gets. If the product only needs "may act for" without hop counts, the cleaner option is a `UNION` over `user_id` alone. That finishes, because the rows then carry only the id.

### low: `queries/acting_for.sql`
Problem: The comment says `UNION (not UNION ALL) drops repeated rows, so mutual delegations cannot loop.` That is false for this query (see the critical finding). A later editor could trust the comment and remove the guard.
Fix: Replace the comment with the reason the path guard exists, and say that `UNION` alone does not stop a loop when a counter column is present.

## Holds up
- `queries/inbox.sql`: the filter on `approver_id` and `status` is led by `claim_approver (approver_id, status)`, so the pending-claim lookup is a search. The `ORDER BY c.id` sorts a small per-user result, and it needs no index.
- `queries/team_rollup.sql`: the recursion uses `UNION ALL`, which is safe because `CHECK (parent_id IS NULL OR parent_id < id)` in `team` forces every parent to have a smaller id. Walking up a chain must end, so no loop can exist. The lookup `team_id IN (SELECT id FROM sub)` is served by `app_user_team`.
- `queries/acting_for.sql`, the first step and the join into `acting`: `delegation_to (to_user, from_user)` serves the `to_user = :user_id` lookup and the recursive join on `d.to_user = a.user_id`. Both are searches, as the query plan shows.
- `schema.sql`, `delegation_to`: the composite key leads with `to_user`, which is the direction the approval walk uses. The primary key `(from_user, to_user)` covers the other direction for uniqueness.
- `schema.sql`, `delegation`: `WITHOUT ROWID` with that composite key is a sound choice for a small link table whose rows are looked up by the pair.

## Not checked
- The application code that writes `delegation` and `claim` is not in the repo, so whether `PRAGMA foreign_keys` is on for every writer is unknown. Foreign keys are not what this review rests on.
- `valid_until` is `TEXT` with no format check. The query compares it to `date('now')` as text, which works for the `YYYY-MM-DD` values in the demo data (all 10 characters, all 2099-12-31). Any writer that stores another date format would break the comparison. This is a question to confirm, not a finding.
- The path-guarded fix was checked on the demo tenant only. Its cost on a larger, denser delegation graph was not measured.
- The 224-of-400 count comes from a Python walk of the delegation graph, not from the SQL query. The query itself was only run for one user before the timeout.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
