Decision: recursive-sql

Walk up the org's parent chain in the existing SQLite database with one recursive query, and pick the highest ancestor-or-self that has a billing account. Do not adopt a graph database for this.

Why:
- The question is a walk up a tree of at most 6 levels, not a general graph problem. The tree is a single parent pointer per org, so each org has exactly one chain upward.
- `org_parent` already indexes `parent_id`, so each step up the chain is an indexed lookup. Each chain is at most 6 rows. The monthly run over 14,000 orgs and the roughly 100 tooltip hovers a day are small work for SQLite.
- The chain is one way and has no branching, so a recursive CTE that joins `org` to its parent is enough. Pick the deepest row that has a `billing_account_id`, and fall back to the org itself when the chain has none. The `COALESCE` in the query below handles the fallback.
- A graph database would add a server and a second copy of the org tree to keep in step with the billing tables, which is a poor trade at this size. An in-memory graph library would also work, but the stdlib-only app does not need a new dependency for a parent-pointer walk.

Dangling parents (the 412 orgs whose `parent_id` points at a deleted org): a recursive join to `org` simply finds no parent row, so the chain stops at the last org that exists. That matches Finance's call, with no guessing and no default org.

Query shape I checked on a toy in-memory tree (not the real `var/billing.db`, which is not in the working directory):

    WITH RECURSIVE chain(id, parent_id, billing_account_id, depth) AS (
      SELECT id, parent_id, billing_account_id, 0 FROM org WHERE id = :org_id
      UNION ALL
      SELECT p.id, p.parent_id, p.billing_account_id, chain.depth + 1
      FROM chain JOIN org p ON p.id = chain.parent_id
      WHERE chain.depth < 6)
    SELECT COALESCE(
      (SELECT id FROM chain WHERE billing_account_id IS NOT NULL ORDER BY depth DESC LIMIT 1),
      :org_id);

The results on the toy tree were as Finance's rule says. An org under a group with an account, and with no account of its own, is billed to the group. An org whose chain has no account is billed to itself. An org whose parent was deleted is billed to the last org that exists in its chain, and then the rule applies to that chain.

Notes:
- The `depth < 6` guard stops the walk if a cycle ever appears in `parent_id`. The app has no foreign keys enforced, so a cycle would not be rejected on write. A test for cycles would be worth adding.
- Run the query against a copy of the real database before relying on it, since the toy tree is only a check of the shape of the rule.
