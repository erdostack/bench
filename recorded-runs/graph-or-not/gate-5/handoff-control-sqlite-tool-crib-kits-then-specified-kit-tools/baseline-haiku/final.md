I added `sql/kit_tools.sql`. It takes `:kit_id` and returns `(tool_id, qty)` for every tool inside the kit at any depth. Quantities multiply down the nesting, and a tool that appears in several sub-kits or directly in the kit is summed into one row. Sub-kits are not listed, and rows are ordered by `tool_id`.

It is a recursive CTE that walks `kit_line` down from `:kit_id`, carrying the product of quantities along each path. The outer query keeps only items with `kind = 'tool'` and groups by tool.

I checked it on a small in-memory database built from `db/schema.sql`. For a top kit holding 2 of sub-kit A, 4 hammers and an empty kit, where A holds 3 drills, 1 hammer and 2 of sub-kit B, and B holds 5 drills and 1 saw, the query returned 26 drills, 6 hammers and 4 saws. Those match a hand count. Sub-kit A alone returned 13 drills, 1 hammer and 2 saws. An empty kit and a tool id both return no rows.

The query relies on the crib app's guarantee that kits never contain themselves. If a longer cycle (A contains B, B contains A) could ever be stored, the recursion would not terminate. The crib app should refuse that too, or the query should get a depth guard.
