# Roast: catalogue schema (schema/, sql/)

Verdict: Nothing critical, but one high: renaming a category slug cascades into the 60 million row placement table with no index behind the foreign key, so admin renames that run into the 30 second timeout will fail. The rest is sound for this workload, apart from one question about cycles in the category tree. You do not have to rewrite the two queries in the placement path; the rename is the one that needs work.

Judged against:
- PostgreSQL 15, product catalogue (README).
- Sizes: category 18 thousand, product 6.4 million, placement 60 million (README).
- Storefront category pages and search are served by the search service from the change stream and never read Postgres (README).
- Product editor reads and writes a product's categories (sql/product_categories.sql, sql/place_product.sql) (README).
- About 40 category renames per working day, admin requests time out after 30 seconds (README, sql/rename_category.sql).
- Admin category tree loads children one level at a time (README, sql/child_categories.sql).

## Findings

### high: `category.slug`
Renaming a slug is a one-row change in the category table and a 60-million-row job in placement. The keys are the problem, not the statement.
Problem: category.slug is the primary key and the target of placement.category_slug and category.parent_slug, both ON UPDATE CASCADE. Each rename (sql/rename_category.sql, about 40 per working day) rewrites every placement row of that category. placement.category_slug has no index, because the placement primary key leads with product_id, so the cascade must read the whole placement table (60 million rows) to find them. Admin requests time out after 30 seconds, so renames fail on a normal day. No data is corrupted: the transaction rolls back.
Fix: Add a surrogate category.id bigint primary key, keep slug UNIQUE, and reference the id from placement and from parent. A rename then changes one category row. Migration: add the id column, backfill it, add the new foreign keys and their indexes, move sql/ statements to the id, then drop the slug foreign keys. Stopgap, labelled as such: `CREATE INDEX placement_category_slug ON placement (category_slug);` turns the scan into a search, but the renamed category's placements are still all rewritten.

### low: `category.parent_slug`
Question to confirm: the tree is an adjacency list with no check that stops a category becoming its own ancestor. Nothing in the files walks it recursively, and sql/child_categories.sql loads one level at a time, so a cycle is not visible or harmful today. Is a recursive walk planned? If so, add a loop guard to that query, or a trigger that rejects a cycle.

## Holds up
- `placement` primary key (`product_id`, `category_slug`): leads with product_id, which serves sql/product_categories.sql and the upsert in sql/place_product.sql. The two-column key also prevents duplicate placements.
- `category_parent` index on `category.parent_slug`: serves sql/child_categories.sql, which is the admin tree's one-level lookup. Keep it.
- `placement.product_id` ON DELETE CASCADE: deleting a product is a search on the primary key prefix, so it is cheap.
- `product.sku` UNIQUE: a natural business key that the schema enforces. Nothing in the files depends on it changing.
- `category.slug` CHECK pattern: stops bad slugs at write time. It is a sound constraint, and it does not change the rename finding.
- The storefront does not read Postgres, so the join in sql/product_categories.sql runs only for editor requests.

## Not checked
- No PostgreSQL server is installed here (psql exists, no server binary), so no plan was run and the rename was not timed. The 30 second timeout is judged from the 60 million row count and a sequential scan, not measured.
- The PostgreSQL behaviour relied on (an ON UPDATE CASCADE over an unindexed referencing column scans that table; a primary key or unique constraint creates an index on its own columns) is from long-stable documentation and was not verified against the 15.x docs in this session.
- Whether the change stream captures the rows changed by the cascade is not in the files, so the search index may or may not see renames. Not a finding here.
- No statement deletes a category, so the cost of deleting one (a scan of placement, which has no index on category_slug) is not rated.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
