# Graph decision

Decision: recursive-sql

The question was how to find, for each org, the highest org at or above it that has its own billing account (falling back to the org itself), and whether that needs a graph database (Tomasz's suggestion), an in-memory graph library, or no graph at all. It is a walk up a parent chain of at most 6 levels, which a recursive query on the existing SQLite database does by primary-key lookups: 14,000 orgs x at most 6 levels = at most 84,000 rows for the whole monthly run.

## Workload facts

- The question asked of the connections: for an org, walk up `parent_id` (org to org, the same kind of thing) to a depth the data decides, and pick the highest ancestor-or-self with `billing_account_id` not NULL; if none has one, the org itself (stated by the user, Finance's rule; billing/invoices.py TODO).
- 14,000 orgs; hierarchies at most 6 levels deep (stated by the user). Depth is bounded by the business at 6.
- Load: one monthly run over all orgs, plus about 100 "who pays for this" tooltip hovers a day (stated by the user). The run is batch; the tooltip is online with no stated latency budget.
- Schema: `org(id PRIMARY KEY, name, parent_id REFERENCES org(id), billing_account_id)` with `CREATE INDEX org_parent ON org(parent_id)`. Walking up enters by `org.id`, the primary key, so each step is one key lookup (db/schema.sql).
- Foreign keys were never switched on: no PRAGMA foreign_keys anywhere in the code, and `billing/db.py` just calls `sqlite3.connect` (billing/db.py). The 2024 cleanup deleted parent orgs without touching their children: 412 orgs have a `parent_id` pointing at an org that no longer exists (stated by the user, counted by Iva). That is 412 / 14,000 = about 2.9% of orgs.
- Finance's rule for those 412: the chain ends at the last org that exists; do not guess where the parent went and do not send them to a default org (stated by the user). With a join from the child to `org.id = parent_id`, a missing parent produces no row, so the walk ends there by itself, with no extra rule needed. The rule is also easy to get wrong the other way (a loop that asks for the parent row and crashes or defaults on None).
- Cycles are not excluded by the schema (no FK enforcement, no CHECK), so the recursive query should cap depth (for example, depth under 20) or use a `UNION` that deduplicates; the 6-level limit is stated but not enforced anywhere.
- Fan-out: not stated and not needed for an upward walk; each org has at most one parent (`parent_id` is a single column).
- Measured on synthetic data, not the real database: SQLite 3.53.1 in memory, 14,000 orgs with parent chains up to 6 levels, about 15% with an account, 400 parent_ids pointing at non-existent orgs, the schema from db/schema.sql. A single recursive query for all 14,000 orgs (picking the highest account-holding ancestor, else self) took about 0.13 s; a one-org tooltip query took about 0.015 ms on average. `EXPLAIN QUERY PLAN` showed `SEARCH o USING INTEGER PRIMARY KEY (rowid=?)` in the recursive step. These are order-of-magnitude numbers for the real data, not measurements of it.
- Required work, derived: at most 14,000 x 6 = 84,000 chain rows for the full run, one pass, once a month.
- unknown: the real `var/billing.db` (not in the repo; `.gitignore` excludes `var/` and `*.db`), so real depth distribution, number of cycles (if any), and real timing were not measured; the latency budget for the tooltip; how long the invoice run may take. Looked in README.md, db/schema.sql, billing/, .gitignore.

## Options considered

- graph-database (a dedicated graph store, as Tomasz suggests for the org tree): rejected, because the walk is at most 6 levels over 14,000 orgs, run once a month plus about 100 hovers a day. A second stateful system and a feed from SQLite (which already has orphaned parents that a feed would have to handle) is far more than 84,000 chain rows need.
- in-process-library (loading the orgs into memory and using a graph library): rejected, because it would work at this size but gives nothing the recursive query does not, while adding a load step and a copy of the tree to keep fresh. It stays an alternative if the rule becomes a whole-tree analysis.
- recursive-sql (a recursive CTE up `parent_id` on the existing SQLite database): chosen, because the walk is an ancestor chain of at most 6 levels, each step a primary-key lookup, and the full run came to about 0.13 s on a synthetic 14,000-org tree. The 412 orphans end their chain naturally. Proposed shape: build the chain per org (org id, ancestor id, account, depth), cap depth, then pick the ancestor with an account at the highest depth, else the org itself. Nothing in the code was changed here.
- no-graph (plain joins, no traversal): rejected, because a hierarchy of unknown depth up to 6 cannot be written as one fixed join without hardcoding six self-joins; that is a walk, and the recursive query is simpler. A plain per-org Python loop would also work, but costs one statement per level (the wasteful form the skill lists).

## What would change the decision

- Hierarchies deeper than 6, or the 14,000 orgs growing by orders of magnitude, with the recursive query measured over a budget that Finance or engineering sets (theirs to set) on the real `var/billing.db`, would move this to in-process-library.
- A requirement for whole-tree analysis (for example, subtree totals for every org at once) would also point to in-process-library.
- A tooltip latency budget that the real database misses after checking the plan with `EXPLAIN QUERY PLAN` would first mean fixing the query or index, not a graph store.
- A cycle found in the real data (an org that is its own ancestor) would not change the option, but Finance would need to say what the invoice does there; today the rule is silent.
