# Roast: category hierarchy (migrations/, queries/)

Verdict: No, the reviewer is not right: the recursive queries are safe as written and need no depth limit. A cycle cannot get into `category_parent` through INSERT or UPDATE because `migrations/003_no_cycles.sql` refuses it, and `shop.db` has none. Nothing serious: nothing at all that I can show, so the list of findings is empty.

Judged against:
- Engine: SQLite (README.md); the plans and tests below ran on SQLite 3.53.1 (the version in production is not stated).
- Shape: about 1,800 categories, at most 7 levels deep, a category can have several parents (README.md). `shop.db` (this morning's copy): 1,793 categories, 3,299 `category_parent` links, 12,000 products, deepest chain 7 levels, 1,046 categories with more than one parent.
- Operations: `queries/ancestors.sql` on every product page (hot path, interactive), `queries/descendants.sql` on the category page (README.md). Merchandising writes only through INSERT, UPDATE and DELETE on `category_parent` (README.md).
- Claim under test: "no cycle protection ... Shoes under Trail Running Shoes would recurse forever", add a depth limit of 10 to every recursive query (docs/pr-comment.md).

## Findings

None.

I went in expecting a loop and the schema had already locked the door. The reviewer's scenario is the exact one `migrations/003_no_cycles.sql` is for.

## Holds up
- `category_parent_no_cycle_insert` and `category_parent_no_cycle_update` (migrations/003_no_cycles.sql): before a link is written, they walk everything below the child and refuse the link if the new parent is in that set. I ran this on an in-memory copy of `shop.db`: a 2-cycle (1 under 2 when 2 is under 1), a 3-level cycle, the same via `INSERT OR REPLACE`, `REPLACE` and `INSERT OR IGNORE`, and an UPDATE of `child_id` that closes a loop were all rejected with "this link would create a cycle". `make db` applies the migrations in order, so a rebuilt database has the triggers, and the `shop.db` copy has both triggers too. This is the "something prevents it" case, so the premise of the review does not hold: with the triggers there is nothing for a depth limit to guard. `shop.db` has no cycle (checked by walking all 3,299 links).
- `CHECK (child_id <> parent_id)` on `category_parent`: stops a category being its own parent, the one-row cycle, before the triggers are even needed.
- `queries/ancestors.sql`: the recursive step joins on `category_parent`'s primary key (`child_id`), one index search per level; the plan shows `SEARCH cp USING PRIMARY KEY`. On the deepest category in the sample it returns 27 ancestors, nearest first. `UNION` keeps (id, depth) pairs distinct and `MIN(depth)` per category collapses the multiple-parent paths; the result is bounded by the 7 levels.
- `queries/descendants.sql`: the plan uses `category_parent_by_parent` (`parent_id`) for each step and `product_category` for the products; on category 1 it returns all 12,000 products, each once, because the walk collects category ids and then does one `IN` lookup.
- `product_category`, `category_parent_by_parent`: every foreign-key lookup in the two queries has an index leading with its column.
- A depth limit of 10 would not hurt today (7 levels), but it would turn "a loop is impossible" into "a loop is silently truncated", and it would cut off real categories if the tree grows past it. Optional insurance only, not a defect either way.

## Not checked
- Whether the merchandising tool turns foreign keys on. SQLite does not enforce `REFERENCES` unless each connection runs `PRAGMA foreign_keys = ON`, and nothing in the repo shows that the tool does. The sample has no orphan links and no product pointing at a missing category, so I do not count this as a finding; it is a question to confirm.
- Whether `product.name` is unique: `queries/descendants.sql` orders by `p.name` with no tiebreaker for paging. Names in the sample are all distinct, so I did not file it.
- Writers that rebuild the table by a path other than INSERT or UPDATE (for example dropping the triggers, or a bulk import into a fresh table): none in the repo.
- Production SQLite version; the triggers use only features available in old versions, but I ran on 3.53.1 only.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
