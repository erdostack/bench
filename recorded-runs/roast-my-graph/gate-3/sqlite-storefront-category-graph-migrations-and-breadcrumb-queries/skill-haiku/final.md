Verdict: Nothing serious, and the reviewer is wrong about the cycle risk. The two recursive queries would never finish on a cycle, but `migrations/003_no_cycles.sql` refuses any insert or update that would make a category its own ancestor, and shop.db has no cycles. The depth limit he asks for is optional insurance, not the fix.

Evidence: on a copy of shop.db, the two loop-creating writes were refused with "this link would create a cycle", and a valid second parent was accepted. The deepest ancestor chain is 6 links, inside the README's 7 levels, so a limit of 10 would not cut any current breadcrumb if he wants one anyway.

Low findings only:
- `queries/ancestors.sql`: breadcrumb order among same-depth ancestors is undefined (four at depth 1 for category 108). Fix: add `c.name` to the ORDER BY.
- `queries/ancestors.sql`: the README says it also builds inherited facets; the file does not, and no facet query is in the repo. Question to confirm.
- `queries/descendants.sql`: the paged ORDER BY uses `p.name` with no unique tie-break, and product names are not unique. Nothing fails today. Fix: `ORDER BY p.name, p.sku`.
- `category_parent`: foreign keys are enforced only with `PRAGMA foreign_keys = ON`, and the writer's setting is not in the repo. Question to confirm.

Files:
- /run/work/docs/graph/ROAST.md
- /run/work/findings.json

Not checked: the merchandising tool's connection settings, multi-row trigger behaviour (only single-row writes were tested), and where facets are computed.
