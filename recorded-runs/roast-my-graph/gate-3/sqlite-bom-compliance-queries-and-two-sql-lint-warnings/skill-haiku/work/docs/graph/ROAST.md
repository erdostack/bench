# Roast: bomdb sql/queries.sql and sql/schema.sql

Verdict: Sound. Do not apply either change. `UNION` in `components_of` is what keeps each part listed once: `UNION ALL` would repeat parts in all 20 products in bom.db (56,216 extra rows), and the query has no `DISTINCT` to hide them. A `LIMIT` would cut the customs and REACH list short, because it has to contain every part in the product, and the largest product has 566 distinct parts. The two linter warnings are false positives for these queries. Nothing serious; the two findings are low.

Judged against:
- SQLite, bom.db is last night's copy of the PLM export (README.md)
- `uses(parent, child, qty)`: sub-assemblies are shared, often several times inside one product (README.md)
- The PLM refuses to save a structure that contains itself, so `uses` is always acyclic (README.md)
- `components_of` must list every distinct part anywhere in a product once: "The customs and REACH declarations list each part once" (README.md)
- `exploded_quantities` counts a part once per path, multiplied on the way down (README.md)
- Costing is a batch job, not an interactive path (README.md, with "for costing")

## Findings

### low: `components_of`
Problem: The linter (lint/findings.txt, PERF012 and PERF020) flags the `UNION` and the missing `LIMIT`. Applying its advice would break the query. A CI rule that cannot tell a dedupe from a wasteful one will keep flagging this query, and someone may apply the change.
Fix: Keep `UNION` and do not add `LIMIT`. Suppress PERF012 and PERF020 for this query in the CI linter, with a comment at the query that says why (`UNION` dedupes shared sub-assemblies; the result must hold every part).

### low: `uses_child`
Problem: The index on `uses (child)` is not used by either query in sql/queries.sql. Both queries walk from parent to child, which the primary key `(parent, child)` already serves. The index costs a write on each change to `uses`, and nothing in the repo reads it.
Fix: Keep it if the compliance team plans a where-used query (a child to its parents). Otherwise drop it with `DROP INDEX uses_child;`. If a where-used query is added, check it with `EXPLAIN QUERY PLAN` for a `SEARCH uses USING INDEX uses_child`.

## Holds up
- `components_of`, `UNION` in the recursive term: the `inside(id)` set holds only ids, so `UNION` drops a repeat when a sub-assembly is reached by a second path. That is required to list each part once. Without it, the final `SELECT` has no `DISTINCT` and repeats parts. It also ends whatever the data shape, since the set stops growing.
- `components_of`, the walk itself: `uses` is acyclic by the PLM rule, and bom.db has no cycles (checked by a depth-first walk). The `CHECK (parent <> child)` removes self-loops. The recursion needs no depth guard here.
- `exploded_quantities`, `UNION ALL`: it counts each path separately, which is what the README asks for. Its row count equals the number of root-to-part paths: about 3,100 to 3,900 rows per product on bom.db, with a maximum depth of 4. Its totals match an independent calculation of path-weighted quantities for all 20 products (0 mismatches). It terminates because `uses` is acyclic. If the structure becomes much deeper or more shared, the row count grows with the number of paths, so recheck this query then.
- `uses (parent, child)` primary key with `WITHOUT ROWID`: lookups by parent are searches on the leading column, which both recursive joins use (`WHERE parent = :product` and `u.parent = i.id`).
- `schema.sql`, `part.number UNIQUE` and `kind` CHECK: the constraints match the README's three kinds.
- `part.substances`: each value is one substance name (DEHP, cadmium, BPA, lead; no separators in bom.db), and the queries return it whole. Nothing searches inside it, so it is not a packed list.

## Not checked
- No query was edited, and bom.db was opened read-only. Plans were read with the Python `sqlite3` module on an in-memory copy of bom.db. The `EXPLAIN QUERY PLAN` output for the two queries was not printed.
- The CI linter's rule definitions were not in the repo, so the description of PERF012 and PERF020 is taken from lint/findings.txt alone.
- Whether a where-used query exists outside this repo (the compliance team's tooling): the repo does not show one.
- Growth of the export is not stated, so the row count of `exploded_quantities` is judged at the current size only.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
