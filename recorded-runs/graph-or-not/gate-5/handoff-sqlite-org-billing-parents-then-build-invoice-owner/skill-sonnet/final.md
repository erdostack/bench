Added `invoice_owner(conn, org_id)` to `billing/invoices.py`, and nothing else. I did not touch the invoice run or the tooltip, and I left the TODO comment in place.

It follows the decision in `docs/graph/DECISION.md` (recursive SQL on the existing SQLite db) and Finance's rule recorded there:
- It walks up `parent_id` with one recursive query. The org itself counts as the start of the chain.
- It returns the highest org on that chain that has its own `billing_account_id`. If none has one, it returns `org_id` itself.
- A `parent_id` pointing at a deleted org (the 412 orphans from the 2024 cleanup) ends the chain at the last org that exists. There is no default org.
- The walk stops at 20 levels, because foreign keys are off and the schema does not forbid cycles. Real hierarchies are at most 6 deep.
- If `org_id` does not exist, it returns `None`.

I checked it on a small in-memory SQLite db built from `db/schema.sql`. The cases were a nested chain with accounts at several levels, a chain with no account, orphaned parents (with and without an account), a self-cycle and a missing org. All returned what the rule says. I did not run it against the real `var/billing.db`, which isn't in the repo.

The decision doc leaves open what the invoice should do if the real data contains a cycle. With the depth cap the function still returns an answer, but Finance should confirm it is the right one.
