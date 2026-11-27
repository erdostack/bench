# Roast: schema.sql and queries/ (approvals, delegation chains)

Verdict: Critical, and it is the inbox timeout: `queries/acting_for.sql` never finishes for anyone who sits in a mutual delegation, because its `UNION` cannot stop a loop once each row carries a hand-off counter. Everything else in the files is sound or `low`.

Judged against:
- Engine: SQLite, version of the demo database not stated in the repo; checked here with SQLite 3.53.1 (README.md does not name an engine; `approvals.db` is a SQLite file).
- Size: `approvals.db` is the demo tenant, 400 people (README.md). Counted in the file: 40 teams, 400 users, 324 delegations, 2000 claims.
- Delegations "come in pairs inside a team" and chains are allowed (README.md). In the file, 242 of the 324 delegation rows have their reverse also stored, and every row has `valid_until` = 2099-12-31.
- `queries/acting_for.sql` runs on every approval inbox page load (README.md): interactive, hot path.
- `queries/team_rollup.sql` runs for the monthly org report (README.md): batch.
- Production tenant sizes: not stated.

## Findings

### critical: `queries/acting_for.sql`
The comment says "UNION (not UNION ALL) drops repeated rows, so mutual delegations cannot loop". The database read the comment, nodded politely and looped until the browser gave up. That is a very expensive way to say hello.
Problem: When the approval inbox runs `queries/acting_for.sql` for a user inside a mutual delegation, which the README says is the usual case ("most delegations come in pairs"), the recursive part carries `handoffs + 1` in every row. Going round a pair produces (Ben, 1), (Ana, 2), (Ben, 3), (Ana, 4) and so on: every row is new, so `UNION` removes nothing and the recursion never ends. Run read-only on `approvals.db`: user 128 (who can reach only 3 people) was still running after 10 seconds when I interrupted it, and 35 of the first 60 users did not finish within 1 second each. That is the "some people" whose inbox times out; the others are users nobody delegates to, whose walk has no loop. Nothing in `schema.sql` prevents it: `CHECK (from_user <> to_user)` only blocks self-delegation, and `PRIMARY KEY (from_user, to_user)` allows both directions.
Fix: Bound the walk by the only thing that can bound it: a chain never needs more hand-offs than there are people, so add the cap in the recursive step and keep `UNION`:
```sql
WITH RECURSIVE acting(user_id, handoffs) AS (
    SELECT from_user, 1
    FROM delegation
    WHERE to_user = :user_id AND valid_until >= date('now')
    UNION
    SELECT d.from_user, a.handoffs + 1
    FROM delegation d
    JOIN acting a ON d.to_user = a.user_id
    WHERE d.valid_until >= date('now')
      AND a.handoffs < (SELECT count(*) FROM app_user)
)
SELECT u.email, MIN(a.handoffs) AS handoffs
FROM acting a
JOIN app_user u ON u.id = a.user_id
WHERE a.user_id <> :user_id
GROUP BY u.email
ORDER BY handoffs, u.email;
```
I ran this for all 400 users in `approvals.db` and compared with a plain breadth-first search in Python: no differences, 0.2 seconds in total, largest result 8 people. If the business wants a shorter chain limit, replace the subquery with that number (and say it in the README). Fix the comment in the file: the `UNION` alone does not stop loops when a counter is in the row. Tested on SQLite 3.53.1; the recursive-CTE syntax is the same in older SQLite.

## Holds up
- `queries/team_rollup.sql` (`WITH RECURSIVE sub`): the walk cannot loop, because `CHECK (parent_id IS NULL OR parent_id < id)` in `team` forces every parent to have a smaller id, so the tree is acyclic and depth is bounded by the number of teams. `UNION ALL` is therefore correct, and the headcount on the demo data is right (team 1 gives 400, all users). It is a monthly batch report on 40 teams; SQLite builds a temporary index on `team.parent_id` for each run, which costs nothing here. Would change if: teams grow to many thousands and the report becomes frequent, then add `CREATE INDEX team_parent ON team(parent_id);`.
- `queries/inbox.sql`: `claim_approver` (`approver_id`, `status`) leads with both filtered columns; the plan is a SEARCH on it plus a primary-key lookup of the owner. It lists claims "as themselves" by its own header, so not including delegated claims is its stated job, not a gap.
- `delegation_to` index on `delegation(to_user, from_user)`: the recursive step looks up delegations by `to_user`, which the primary key (`from_user`, `to_user`) cannot serve; the plan shows a SEARCH using `delegation_to`.
- `valid_until` as TEXT compared with `date('now')`: every stored value is an ISO date (2099-12-31), so string comparison orders correctly. Would change if: a value in another format is ever written.

## Not checked
- Production data volumes and its delegation shape: only the 400-person demo copy exists here. A larger tenant makes the loop worse, never better.
- I interrupted the unbounded query after a time limit, so "never finishes" rests on the data (each lap adds a distinct counter value) and not on waiting forever.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
