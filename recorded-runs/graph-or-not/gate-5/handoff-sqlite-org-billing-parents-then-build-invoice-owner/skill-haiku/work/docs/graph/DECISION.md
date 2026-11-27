# Graph decision

Decision: recursive-sql

Billing asked whether the nested-organisation invoice routing needs a graph database, an in-memory graph library, recursive SQL or no graph. Finding the payer is a walk up the parent chain of at most 6 levels to the highest organisation with its own billing account, so it is a traversal, but it is short, stays in the SQLite file billing already runs, and touches at most 6 rows per organisation. The finding it turns on: the monthly run reads at most 14,000 x 6 = 84,000 chain rows, and the tooltip about 100 x 6 = 600 rows a day.

## Workload facts

- 14,000 organisations (stated by the user)
- Hierarchies are at most 6 levels deep (stated by the user)
- The invoice run goes over all organisations once a month (stated by the user)
- The "who pays for this" tooltip gets about 100 hovers a day (stated by the user)
- Finance's rule: an org's usage is invoiced to the highest organisation above it, or the org itself, that has its own billing account; if no one in its chain has an account, the invoice goes to the org itself (stated by the user)
- Foreign keys are not enforced anywhere in the app (no PRAGMA foreign_keys in the code); the 2024 cleanup deleted parent orgs without their children; 412 orgs have a parent_id that points at a deleted org (stated by the user, from Iva's count)
- Finance's ruling for the 412: the chain ends at the last organisation that exists; no guessing and no default org (stated by the user)
- Derived: the chain for one org has at most 6 organisations (the depth limit above); the monthly run is at most 14,000 x 6 = 84,000 chain rows, and the tooltip is at most 100 x 6 = 600 rows a day (from the stated counts, multiplied out)
- Schema `db/schema.sql`: `org` (id primary key, parent_id, billing_account_id) with index `org_parent` on parent_id; `billing_account`; `usage_line` (org_id, month, amount)
- The current code has only `org()`, `usage_total()` and the TODO; no payer lookup exists yet (`billing/invoices.py`)
- SQLite is the database (`billing/db.py`, `README.md`); the file `var/billing.db` is gitignored and not in the repo, so real counts and the real chain shape are not available
- Measured (synthetic, not the real billing data): in-memory SQLite 3.53.1 on Python 3.13.18, a generated forest of 14,000 organisations with depth at most 5 below the roots, 412 parent_ids pointing at deleted ids, and about 15% of organisations holding a billing account. The recursive query below, run once per organisation (14,000 calls), matched a plain Python walk that stops at the last existing organisation for every organisation (0 mismatches). The full pass took about 0.29 s. `EXPLAIN QUERY PLAN` showed primary-key lookups on `org` for each step (`measured`: inline script run in memory; nothing written to disk)
- unknown: the real chain depth distribution and how many organisations have a billing account; the billing file is not in the repo
- unknown: whether any parent_id cycles exist in the live data; the recursive query needs a depth guard for that case

The query used in the measurement, for organisation `:x`:

```sql
WITH RECURSIVE chain(id, parent_id, billing_account_id, depth) AS (
  SELECT id, parent_id, billing_account_id, 0 FROM org WHERE id = :x
  UNION ALL
  SELECT o.id, o.parent_id, o.billing_account_id, c.depth + 1
  FROM org o JOIN chain c ON o.id = c.parent_id
  WHERE c.depth < 32)
SELECT COALESCE((SELECT id FROM chain WHERE billing_account_id IS NOT NULL
                 ORDER BY depth DESC LIMIT 1), :x);
```

The depth guard of 32 is a safety cap and not a business limit; the business limit is 6 levels as stated. The query takes the highest organisation with an account (largest depth), and falls back to `:x`. Because the walk stops at a missing parent, the 412 dangling chains end at the last organisation that exists, as Finance asked.

## Options considered

- graph-database (a dedicated graph store, as Tomasz suggested): rejected, because the walk is at most 6 steps over 14,000 organisations, read once a month and about 100 times a day, and the SQLite file already has the key lookups needed (see the measurement). A server would add a second copy of the org tree that can drift from billing's own data, plus a new query language, for a walk this short.
- in-process-library (the org tree loaded into memory with a graph library): rejected, because the rung above holds. It would work at this size, but it adds a copy of the tree in each process and a reload step whenever organisations change. It remains the fallback if the chain is ever deeper than the limit.
- recursive-sql (recursive queries on the SQLite file billing already runs): chosen, because the chain is a walk to a data-dependent depth of at most 6, starting from one organisation, over a database already operated, and the required work is at most 84,000 chain rows per monthly run (see the derived figures and the measurement, 0.29 s for all 14,000 organisations).
- no-graph (plain joins, no traversal): rejected, because finding the highest organisation with an account needs the whole chain above the organisation, which is a walk of more than one step; a fixed join would only cover one level.

## What would change the decision

- Chains deeper than the stated 6 levels appear in the live data, or the business needs a depth beyond what the recursive query handles with the index, measured on the real file; this is for the billing owner to confirm.
- The monthly run or the tooltip starts running many times per second (for example, per usage line instead of per organisation and per hover), so that the per-organisation walk becomes a measured cost on the real file; this would move the choice toward in-process-library with a snapshot reloaded when organisations change.
- A decision to store the resolved payer on each organisation, updated when the tree or accounts change; that would be a precomputed table rather than a graph store, and would be a choice for billing to make with its own write rate.
- Any evidence that the org tree needs to be queried by relations other than parent (for example, shared ownership across branches); that would be re-examined.
