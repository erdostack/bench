# Roast: schema.sql and queries/ (approver service)

Verdict: Sound, and the reviewer is wrong: `queries/final_approver.sql` does not spin on mutual delegations, so you can push back. The recursive step already has a cycle guard, `WHERE d.delegate_id <> ALL (c.path)`, which stops the walk the moment the chain would revisit someone. Nothing is rated critical, high, medium or low.

Judged against:
- Engine: PostgreSQL 16 (README.md). Checked on PostgreSQL 16.15, a throwaway local cluster.
- Rule: a person hands approvals to one delegate, "at most one row per person", and the delegate may hand on too (README.md).
- Loops are expected: "two people on leave the same week, each delegating to the other"; the query must stop at the last person before the repeat, and that person approves (README.md).
- Load: `final_approver.sql` is called once per submitted claim, about 2,000 a day (README.md). Table sizes: not stated.

## Findings

None.

A schema where the loop case is written down in the README, guarded in the query, and bounded by a primary key. Frankly suspicious. I looked for the catch and the catch was the reviewer's comment.

## Holds up
- `queries/final_approver.sql` (the recursive CTE `chain`): the reviewer's two claims, "no depth limit" and "UNION ALL keeps every row", are both true of the syntax and neither is the failure. Failure test: when it runs on a mutual delegation (A to B, B to A) it should spin forever. It does not: each recursive step is allowed only if `d.delegate_id <> ALL (c.path)`, and `path` carries every person already visited, so a person can be added at most once and the walk ends after at most one step per person. In addition, `delegate.user_id` is the primary key, so each person has at most one outgoing delegation and the chain is a single line, not a fan-out; there is nothing to multiply. I ran it on PostgreSQL 16.15 with a pair (1 and 2 delegating to each other), a three-person ring (3, 4, 5), an expired delegation (`until` in the past), a chain that just ends, and a person with no delegation: every call returned at once. From 1 it returns user 2 with 1 hand-off, from 2 it returns user 1 with 1 hand-off, the ring from 3 returns user 5 with 2 hand-offs, an expired delegation stops at the delegator (0 hand-offs). That is exactly the README rule ("stops at the last person before the repeat"). A depth limit or `LIMIT` inside the CTE is optional insurance only. Be careful with a `LIMIT` inside: it would not make the answer more correct, and the final `ORDER BY cardinality(path) DESC LIMIT 1` is needed to pick the end of the chain. Moving the walk into application code would add a round trip per hop to replace a bounded loop that already works. Would change if: `delegate` stopped being one row per person (the primary key on `user_id` is what keeps the chain a line).
- `ORDER BY cardinality(path) DESC LIMIT 1` in `queries/final_approver.sql`: with one outgoing delegation per person every length occurs once, so the longest path is unambiguous and the result is never a random pick among ties.
- `delegate.until` with `d.until >= current_date`: an expired delegation ends the chain, as the schema comment says ("until the given date"), and the date itself still counts.
- `claim_approver` (partial index on `approver_id` where `status = 'submitted'`) with `queries/my_queue.sql`: the query's `status = 'submitted'` matches the index predicate and the plan uses it (checked on 200,000 generated claims: a bitmap scan on `claim_approver`, then a small sort). `queries/assign_approver.sql` finds the claim by primary key.
- `delegate_by_delegate`: no query in the repo reads it, but it backs the foreign key from `delegate.delegate_id` to `app_user(id)`, which PostgreSQL does not index on its own, so deleting or updating a user does not scan `delegate`. Keep it. Would change if: users are never deleted and nothing looks delegations up by delegate, then it is optional.
- `claim.approver_id` is nullable: a claim has no approver until `queries/assign_approver.sql` runs, and `my_queue.sql` only looks for a specific approver, so a null is correct before assignment.

## Not checked
- Production volume of `app_user` and `delegate`: not stated; the checks used generated data of 1,000 users and 200,000 claims.
- Nothing in the repo shows who calls `queries/assign_approver.sql` or whether it is given the output of `final_approver.sql`; no statement or constraint ties the two, which is a design choice and not shown to be a defect.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
