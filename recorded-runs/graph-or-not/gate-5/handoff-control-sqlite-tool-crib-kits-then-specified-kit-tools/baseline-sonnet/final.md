I added `sql/kit_tools.sql`. It takes `:kit_id` and returns `(tool_id, qty)`, one row per tool, ordered by `tool_id`.

- Quantities multiply down the nesting, so 2 sub-kits of 3 drills each gives 6 drills. They add up where the same tool shows up in more than one sub-kit or directly in the kit. Sub-kits are not listed.
- I tested it on a small in-memory database with nested kits, the same tool at several levels, and a tool packed directly in the top kit. The totals matched my hand calculation. A kit id with no lines returns no rows.
- Unlike the existing `sql/kit_all_tools.sql`, this one has no depth limit. That file stops at depth 8. I left the limit out because you said kits never contain themselves, and a fixed limit would silently drop tools in deeper nesting. If bad data ever did create a cycle, this query would not stop, so the crib app's check is what protects it.
