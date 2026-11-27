# Roast: approver schema and queries (final_approver, assign_approver, my_queue)

Verdict: Nothing serious. The reviewer is wrong that `queries/final_approver.sql` spins forever on mutual delegations. The `WHERE d.delegate_id <> ALL (c.path)` filter stops the walk at the first repeat, and `delegate.user_id` is the primary key, so each person has at most one outgoing delegation. The walk is therefore a single line that ends after at most one step per person. You can push back. A depth cap is not needed to stop the loop. The two findings below are low.

Judged against:
- PostgreSQL 16 (README.md)
- Normally the claimant's line manager approves. A person on leave hands approvals to one delegate, `delegate` has at most one row per person, and the delegate may hand on too (README.md, schema.sql)
- Mutual delegations (A to B and B to A) are expected and the README says the query stops at the last person before the repeat (README.md)
- Called once per submitted claim, about 2,000 a day (README.md)

## Findings

### low: `queries/final_approver.sql`
Problem: Question to confirm: the query does not exclude the claimant. If a manager on leave delegates to one of their own reports, and that report is the claimant, the walk can end on the claimant, who then approves their own claim. The files do not state whether self-approval is allowed. `assign_approver.sql` does not check it either.
Fix: If self-approval is not allowed, add `AND d.delegate_id <> $2` to the recursive join (or check it in the application) and return the next person up, or reject the claim. If it is allowed, say so in the README so the question does not come up again.

### low: `delegate_by_delegate`
Problem: The index on `delegate (delegate_id)` is not used by any query in the repo. `final_approver.sql` finds the next hop by `user_id`, which the primary key already serves. Nothing in the files asks "who has delegated to this person". The index costs a write on each delegation change, which is rare.
Fix: Drop the index with `DROP INDEX delegate_by_delegate;` unless a query that filters on `delegate_id` is added. If one is added, keep the index and confirm the plan with `EXPLAIN`.

## Holds up
- `queries/final_approver.sql`, the recursion: the filter `d.delegate_id <> ALL (c.path)` stops the walk at a repeat, so the mutual-delegation case from the review ends in one extra step. The `delegate` primary key `user_id` allows at most one outgoing hop per person, so the recursive set is one line, and its length is bounded by the number of users. The `UNION ALL` is therefore not a risk. A depth cap would be optional insurance.
- `queries/final_approver.sql`, the join condition `d.until >= current_date`: each hop is checked for expiry, so an expired link ends the chain before it is followed.
- `queries/final_approver.sql`, `ORDER BY cardinality(path) DESC LIMIT 1`: with a single line of rows, the deepest row is the last person on the chain, which is the approver the README names.
- `schema.sql`, `delegate` `CHECK (user_id <> delegate_id)`: rejects the one-step self-delegation.
- `queries/my_queue.sql`: the filter `c.approver_id = $1 AND c.status = 'submitted'` matches the partial index `claim_approver (approver_id) WHERE status = 'submitted'`, because the literal in the query implies the index predicate.
- `queries/assign_approver.sql`: a primary-key update, conditional on `status = 'submitted'`, so an approved or rejected claim is not overwritten.

## Not checked
- Nothing was run. PostgreSQL is not installed on this machine, so no plan or result was produced. The termination argument was checked by emulating the walk in Python: a mutual pair from manager 1 returns user 2 at one hop in two steps, and a three-person cycle returns user 3 at two hops in three steps.
- Whether `final_approver.sql` runs inside the claim-submission transaction. The reviewer says it "locks up claim submission", and the files do not show the caller. The termination argument does not depend on it.
- Whether a loop could be formed by data written outside the files. The `delegate` primary key limits each person to one outgoing row, which is what the argument rests on.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
