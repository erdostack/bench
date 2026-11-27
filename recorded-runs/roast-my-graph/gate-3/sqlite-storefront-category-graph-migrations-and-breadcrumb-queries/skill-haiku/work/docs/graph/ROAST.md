# Roast: category breadcrumbs (migrations/, queries/)

Verdict: Nothing serious, and the review is wrong about the cycle risk. Both recursive queries would never finish on a cycle, but `migrations/003_no_cycles.sql` refuses any insert or update that would make a category its own ancestor, and the data has no cycles. A depth limit is optional insurance, not the fix the review asks for. The real guard is the trigger pair, and it works: on a copy of `shop.db` the two loop-creating writes were refused and a valid second parent was accepted.

Judged against:
- README.md: about 1,800 categories, at most 7 levels deep; a category can have several parents; merchandising writes `category_parent` with INSERT, UPDATE and DELETE through SQL; `make db` applies `migrations/` in order to an empty database.
- Measured on `shop.db` (SQLite 3.53.1, read-only): 1,793 categories, 3,299 parent links, 12,000 products. 1,046 categories have two or more parents. The deepest ancestor chain is 6 links, which is 7 levels counting the top. No category reaches itself, no link is a self-link, and no link points at a missing category.
- Interactive: `queries/ancestors.sql` on every product page; `queries/descendants.sql` on each category page, paged.
- Writers: merchandising SQL against `category_parent`. The triggers apply to every writer.
- Stated invariant: a category can sit under several parents (README).

## Findings

### low: `queries/ancestors.sql`
The breadcrumb query orders by `depth` only. Categories at the same depth come back in an order the query does not define. For example, the ancestors of category 108 include four at depth 1 (Bags men, Base-Layer bags, Running socks, Waterproof jackets), and their order is whatever the plan produces.
Problem: breadcrumb order among equal-depth ancestors is not specified, so the same page can show them in a different order after a plan change.
Fix: `ORDER BY depth, c.name` (or `c.slug`, which is unique in the shipped data).

### low: `queries/ancestors.sql`
The README says `ancestors.sql` "builds the breadcrumbs and the inherited facets on every product page". The file builds only the breadcrumbs. No facet query exists in the repo.
Problem: the README describes a facet computation that is not in the files. Either the facets are computed elsewhere (not in this repo) or the README is out of date. This is a question to confirm, not a defect in the query.
Fix: either add the facet query to `queries/` or correct the README line.

### low: `queries/descendants.sql`
The page is `ORDER BY p.name LIMIT :page_size OFFSET :offset`, with no unique tie-break. `product.name` is not unique: `migrations/002_products.sql` makes only `sku` unique. When two products in a category subtree share a name, their order between pages is undefined, so a product can appear on two pages and another can be skipped.
Problem: no duplicate names exist in the shipped data (checked: 0), so nothing fails today. This is a question to confirm about whether duplicate names are possible.
Fix: `ORDER BY p.name, p.sku`.

### low: `category_parent`
`migrations/001_categories.sql` declares `REFERENCES category(id)` on both columns. SQLite enforces a foreign key only on connections that set `PRAGMA foreign_keys = ON`, which is off by default. The merchandising tool's connection setting is not in the repo. A link to a missing category would be stored without error, and `queries/ancestors.sql` inner-joins `category`, so that link would silently vanish from the breadcrumbs.
Problem: nothing in the repo proves that every writer enables foreign keys. The shipped data has no such rows (checked: 0 dangling links), so this depends on whether the tool can write a bad id. This is a question to confirm.
Fix: set `PRAGMA foreign_keys = ON` on every connection that writes, or add a `BEFORE INSERT` and `BEFORE UPDATE` trigger that checks the parent exists.

## Holds up
- `category_parent (child_id, parent_id)` primary key with `WITHOUT ROWID`, and `category_parent_by_parent (parent_id, child_id)`: `ancestors.sql` plans as `SEARCH cp USING PRIMARY KEY (child_id=?)`, and `descendants.sql` plans as a search on `category_parent_by_parent`. Both walks are index searches at each step.
- `product_category (category_id)`: the category page's product lookup is a search (`SEARCH p USING INDEX product_category (category_id=?)`).
- `category_parent_no_cycle_insert` and `category_parent_no_cycle_update` (`migrations/003_no_cycles.sql`): each refuses a link whose parent is already a descendant of its child. Tested on an in-memory copy of `shop.db`: inserting a link that closes a two-level loop was refused with "this link would create a cycle", an update that closes a loop was refused the same way, and a valid second parent for a category was accepted. After those tests the copy still had no cycles. The trigger's own recursion uses `UNION` over the id alone, so it finishes on any data.
- No depth bound and no visited set in `ancestors.sql` or `descendants.sql`: per the traversal check, the schema bounds the shape (no loop can be written through the migrated write path), the data has no loop, and the deepest chain is 6 links. Verdict for this part: safe as written. A bound such as `WHERE u.depth < 10` in each recursive step would stop the walk and would not cut any current breadcrumb, so it is optional insurance, not a requirement. It is the only protection left if the triggers are ever dropped or a snapshot from before migration 003 is restored.
- `descendants.sql`: the `IN (SELECT id FROM down)` form returns each product once, however many paths lead to its category. Its results are not affected by multiple parents.
- Ancestor and descendant timings on the sample: the ancestors query for category 108 took about 0.2 ms, and the first page of descendants for root category 1 took about 14 ms. The product count (12,000) is small, so the sort in the descendants plan is not a concern at this size.

## Not checked
- No writes were run against `shop.db`. The trigger tests ran on an in-memory copy made with the SQLite backup API.
- Only single-row writes were tested. The triggers check each row against the table as it stands when that row is written, which should cover multi-row statements, but this was not tested.
- Whether the merchandising tool sets `PRAGMA foreign_keys`, and whether the storefront's connections do anything beyond the defaults. Neither is in the repo.
- Where facets are computed, if anywhere.
- Traffic and page-load targets are not stated, so no time budget is claimed.
- The repo has no tests.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
