# Roast: supplymap upstream query (PostgreSQL 16)

Verdict: Not sound. The risk page spins because `queries/upstream_tiers.sql` never finishes whenever a supply ring sits upstream of the plant. The recursive `UNION` cannot stop it: every pass produces a row with a higher `tier` and a longer `path`, so no row ever repeats. The page is only sometimes slow because only plants with a ring upstream trigger it. Fix the statement's shape, not the timeout: walk companies, not routes.

Judged against:
- Engine: PostgreSQL 16 (`docker-compose.yml`, image `postgres:16.4`). No server was available here, so every Postgres behaviour below is from the documentation as recalled and is unverified.
- Size: about 14,000 companies and 90,000 supply links (`README.md`).
- Interactive path: buyers open the page many times a day; each open runs `queries/upstream_tiers.sql` through `app/risk_page.py` (`README.md`).
- Stated structure: the graph has "plenty of loops", including trading rings, and a supplier can also be a customer of the same company (`README.md`).
- Stated result: for one plant, every company upstream, its lowest tier, and one breadcrumb path (`README.md`, comment in `queries/upstream_tiers.sql`).
- Constraint: `supplies` allows `supplier_id <> customer_id` only, so rings of length two or more are allowed (`schema.sql`).

## Findings

### critical: `queries/upstream_tiers.sql`
The recursive step never stops on a ring.
Problem: The recursive part joins `upstream` back to `supplies`, and each row carries `tier` and `path`. `UNION` removes only identical rows, and a ring returns to the same company at a higher tier with a longer path, which is a new row each time. Trace a ring with plant 1 buying from 2, and 2 and 3 buying from each other: each pass adds one row (2 at tier 1, 3 at tier 2, 2 at tier 3, and so on). Checked by emulating the statement's `UNION` semantics on that small graph: the row count grew by one each iteration and never emptied. The statement therefore runs until the database kills it. The trigger is in the files: a ring upstream of a plant, which the README says exists.
Fix: Stop the cause: the statement tracks routes, not companies. Find the upstream set with a recursion over `company_id` alone, which terminates because `UNION` on one column can produce at most one row per company:
```sql
WITH RECURSIVE upstream (company_id) AS (
    SELECT supplier_id FROM supplies WHERE customer_id = $1
  UNION
    SELECT s.supplier_id FROM supplies s JOIN upstream u ON s.customer_id = u.company_id
)
SELECT company_id FROM upstream;
```
Then take each company's lowest tier and one breadcrumb path with a breadth-first walk in the application, keeping a visited set and a parent pointer per company (one query per tier, each on the `supplies` primary key `(customer_id, supplier_id)`). A depth cap such as `WHERE u.tier < 20` in the existing statement stops the loop, but it is a stopgap: the route rows still multiply.

### high: `queries/upstream_tiers.sql`
The statement produces one row per route, not per company.
Problem: The `path` array makes each distinct route a separate row. Where companies can be reached by several routes (a diamond: two routes to the same supplier), the row count multiplies with each diamond. The `DISTINCT ON` picks one row per company only after every route has been generated. With 14,000 companies and 90,000 links, a multi-tier supply graph has far more routes than companies, so the statement cannot finish at the stated size even without a ring. The files do not give the number of routes; the trigger is the stated structure (suppliers that also buy from their customers, multi-tier supply).
Fix: The same as the critical item: a company-level walk with a visited set, and a parent pointer per company for the breadcrumb. Do not fix it by adding a `LIMIT` or a higher timeout.

### low: `app/risk_page.py` (`upstream`)
Problem: `cur.execute` has no statement timeout and no row limit, so a runaway statement holds a connection until something outside the app kills it. That is the "spins until the connection is killed" the user sees. A guard would limit the damage but would not fix the query.
Fix: Optional insurance once the statement is fixed: set `statement_timeout` on the connection that serves the risk page (`SET statement_timeout = '5s'`) so a regression fails fast instead of holding the connection.

### low: `queries/upstream_tiers.sql`
Problem: A ring can bring the plant back into its own upstream list, so the plant can appear as its own supplier with a breadcrumb that starts and ends at it. Whether the page should show the plant is not stated in the files, so this is a question to confirm.
Fix: If the plant should not appear, drop it in the breadcrumb walk (or in the final select with `WHERE company_id <> $1`). The company-level walk above can also skip it because the plant is already visited at tier 0.

## Holds up
- `supplies` PRIMARY KEY `(customer_id, supplier_id)`: serves the first step of the recursion and `queries/direct_suppliers.sql` (`WHERE s.customer_id = $1`), and the recursion's `s.customer_id = u.company_id` join. The fixed walk uses the same key.
- `supplies_by_supplier (supplier_id, customer_id)`: serves the reverse join in `queries/flagged_suppliers.sql` (`s.supplier_id = f.company_id`).
- `CHECK (supplier_id <> customer_id)`: blocks direct self-supply, so the two-company ring is the shortest loop; longer rings are not blocked and are not a problem for the fixed walk.
- `risk_flag` PRIMARY KEY `(company_id, reason)`: sound for the per-company flags; `queries/flagged_suppliers.sql` returns one row per plant-supplier-reason, which is the intent.
- `direct_suppliers.sql` and `flagged_suppliers.sql`: no loop, one join per table, and both key lookups are served by the indexes above. Not a risk.

## Not checked
- Nothing was run on PostgreSQL: no server is available here, so the claims about `UNION`, recursion and `statement_timeout` are from the documentation as recalled (`engines.md` marks them unverified). The emulation of the statement's semantics was done in Python on a three-company ring.
- The real data was not available (no database file in this repo), so the number of routes and whether a given plant has a ring upstream are not known.
- PostgreSQL's `CYCLE` clause (version 14 and later) stops a path from revisiting a company, but it still enumerates every route, so it is not the fix. Not run.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
