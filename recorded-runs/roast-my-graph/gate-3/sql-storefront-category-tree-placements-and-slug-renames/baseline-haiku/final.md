Honest roast of the catalogue schema. The main problem is that renaming a category is expensive by design, and the admin screen does it about 40 times a working day.

**The big one: slug renames**

- `category.slug` is the primary key, and both `placement` and `category.parent_slug` reference it with `ON UPDATE CASCADE`. A slug is a public, SEO-facing identifier, and it gets renamed. The schema therefore turns a one-row rename into a bulk write across every placement of that category. If the change stream captures `placement`, every product in that category also generates an event.
- `placement.category_slug` has no index. Its primary key starts with `product_id`, so nothing can look up placements by category. Each rename therefore sequentially scans up to 60 million rows to find what to cascade, then rewrites them. That can easily exceed the 30 second admin timeout. I have not measured this; it is what the schema implies. Quick fix: `CREATE INDEX placement_category_slug ON placement (category_slug);`.
- The real fix is to give `category` a surrogate `bigint` id, make `slug` a `UNIQUE` column, reference the id from `placement` and from the parent link, and keep a `slug_history` table so old URLs can redirect. After that a rename is a single-row update.
- `rename_category.sql` keeps no old slug and no audit row, and it sets no timeout. Renamed URLs break silently.

**Other problems**

- Nothing stops a category from being its own parent or from forming a cycle. The admin tree would loop, and any recursive query would never end. Add a `CHECK (parent_slug IS DISTINCT FROM slug)` now, and reject cycles on write.
- The slug pattern accepts leading or trailing hyphens and runs of hyphens. Tighten it.
- `placement.position` has no uniqueness rule within a category, so the order of tied products is undefined.
- `category_parent` indexes only `parent_slug`, while `child_categories.sql` sorts by `title`. This is fine at 18 thousand rows, so I rated it low.

**What is fine**

- `place_product.sql` and `product_categories.sql` use the primary key correctly, and the upsert is sound.
- `placement.product_id` is covered by the primary key, so product deletes cascade without a scan.
- The storefront reads from the search index and not from Postgres, so the schema does not sit on the customer read path.

The full list, with severities and fixes, is in `findings.json` in the repo root.
