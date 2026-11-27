# Roast: catalogue schema (schema/ and sql/)

Verdict: Mostly sound, with one high finding. The slug is both the primary key and the thing merchandisers rename, so every rename rewrites that category's rows in `placement`. It must first find them with no index that leads with `category_slug`, in a 60 million row table, under a 30 second admin timeout. Everything else holds up.

Judged against:
- Engine: PostgreSQL 15 (README.md). Exact minor version: not stated.
- Sizes: category 18 thousand, product 6.4 million, placement 60 million (README.md).
- Reads: the storefront category pages and search never read Postgres; the search service is re-indexed from the change stream (README.md).
- Interactive: the product editor reads and edits a product's categories (`sql/product_categories.sql`, `sql/place_product.sql`); the admin tree loads children one level at a time (`sql/child_categories.sql`).
- Writes: about 40 category slug renames per working day, admin requests time out after 30 seconds (README.md, `sql/rename_category.sql`).
- Invariants stated: placements and child categories follow a rename through ON UPDATE CASCADE (`sql/rename_category.sql`).
- docs/graph/CONTEXT.md: not present.

## Findings

### high: `slug`
The primary key is the one thing marketing is allowed to edit. Forty times a day someone renames a campaign and Postgres has to chase the new name through 60 million rows with a flashlight and no index.
Problem: When `sql/rename_category.sql` runs (`UPDATE category SET slug = $2 WHERE slug = $1`) on `category.slug`, the ON UPDATE CASCADE on `placement.category_slug` must find every placement of that category. The only key on `placement` is `PRIMARY KEY (product_id, category_slug)`, which leads with `product_id`, and no file defines an index leading with `category_slug`. So each rename reads all 60 million rows of `placement` (README: 60 million), then rewrites every matching row and its primary key entry, and also rewrites `parent_slug` on the child categories. All of it runs inside the one admin request that times out at 30 seconds. Product editor writes to the same category's placements wait on those row locks meanwhile.
Fix: Remove the cause by making the key stable (PostgreSQL 15 syntax).
1. `ALTER TABLE category ADD COLUMN id bigint GENERATED ALWAYS AS IDENTITY UNIQUE;`
2. `ALTER TABLE category ADD COLUMN parent_id bigint;` then backfill it from `parent_slug`.
3. `ALTER TABLE placement ADD COLUMN category_id bigint;` then backfill from `category` in batches of about 100 thousand rows, with `CREATE UNIQUE INDEX CONCURRENTLY` on `(product_id, category_id)` built before the swap.
4. In one short transaction: drop the old `placement` primary key, add `PRIMARY KEY USING INDEX` on `(product_id, category_id)`, add `FOREIGN KEY (category_id) REFERENCES category (id)` as `NOT VALID` and validate it afterwards, set both new columns NOT NULL, and drop `placement.category_slug`.
5. Replace the primary key on `category` with `id` and keep `slug` as `NOT NULL UNIQUE` with the existing CHECK; replace `parent_slug` and its index `category_parent` with `parent_id` and an index on it.
6. Change `sql/product_categories.sql`, `sql/place_product.sql` and `sql/child_categories.sql` to use ids.
After this `sql/rename_category.sql` is unchanged and touches one row.
Stopgap only, labelled as such: `CREATE INDEX CONCURRENTLY placement_category_slug ON placement (category_slug);` turns the scan into a search, but each rename still rewrites every placement row and index entry of that category and still holds their locks. It does not remove the cause.

## Holds up
- `placement`: it sits between `product` and `category` but is already a row keyed by the pair, carrying `position`. That is the right shape for a product in several categories with a position in each. Nothing else refers to it. Do not collapse it further.
- `PRIMARY KEY (product_id, category_slug)` on `placement`: leads with `product_id`, which is the filter in `sql/product_categories.sql` and the cascade from `ON DELETE CASCADE` on `product`. The ON CONFLICT target in `sql/place_product.sql` is exactly this key, so the upsert is safe and exact. It does not serve lookups by category, which is the finding above.
- `category_parent`: leads with `parent_slug`, the filter in `sql/child_categories.sql`. No second index is needed. It would be replaced by an index on `parent_id` in the fix above.
- `parent_slug` self-reference: no file walks it more than one level (the README says the admin tree loads one level at a time), so no recursive query exists to guard. If a recursive walk is added, it needs a depth bound or cycle check first.
- `sku` UNIQUE, `slug` CHECK, NOT NULL columns: nothing in the files shows a bad row or a lookup that needs more.

## Not checked
- Nothing was run: no Postgres server or sample data on this machine. The scan and rewrite cost is argued from the DDL and the README sizes, not measured, so the claim is that the rename must read 60 million rows, not that it takes more than 30 seconds.
- PostgreSQL behaviour used: a foreign key does not create an index on the referencing column, and a primary key's multi-column index serves its leading column only. Both are long-stable but were not verified against the PostgreSQL 15 docs here (engines.md marks them unverified).
- How many placements a typical renamed category has is not stated; the 18 thousand categories and 60 million placements average to about 3,300 per category, and real categories will vary.
- Whether the search service stores the slug on products and needs its own re-index after a rename is not in the files.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
