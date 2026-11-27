# Roast: sql/ in bomdb (schema.sql, queries.sql)

Verdict: Sound, and do not apply either linter suggestion: both would break `components_of`. `UNION` is what makes the result list each part once (the README's rule), and a `LIMIT` would silently cut a customs and REACH declaration short. Nothing needs changing in `sql/`; the two warnings in `lint/findings.txt` are false positives for this query.

Judged against:
- Engine: SQLite (README.md: "in SQLite"); checked with SQLite 3.53.1 on `bom.db`, opened read-only.
- Size, counted in `bom.db`: 690 parts (20 products, 270 assemblies, 400 components), 2,890 `uses` rows, deepest structure 4 levels. Production size: not stated.
- `bom.db` is a copy of last night's export (README.md); queries run by the compliance team, frequency not stated: batch / report use.
- Sub-assemblies are shared, "often several times inside one product" (README.md): the same part is reachable by several paths.
- `components_of`: "every distinct part anywhere inside a product. The customs and REACH declarations list each part once." `exploded_quantities`: a part appearing in three places counts three times, times the quantities on the way down (README.md).
- `uses` is always acyclic: the PLM system refuses to save a structure that contains itself (README.md). Checked in `bom.db`: no cycle.

## Findings

None.

Two linter warnings, zero defects. The linter saw a recursive query with `UNION` and a missing `LIMIT` and went for the kill; the query was right the whole time. A database that makes the correct choice and gets a ticket for it. Rare enough to frame.

## Holds up
- `components_of` (`UNION` in the recursive CTE `inside`, lint PERF012): this is the only thing standing between the declaration and duplicates. Failure test: with `UNION ALL`, a shared fastener kit or harness is reached once per path, and each path adds a row. Run on `bom.db` for product 671: `UNION` returns 564 parts, each once; `UNION ALL` returns 3,604 rows for the same 564 parts (about six copies of each on average, and the same for the other products: 3,081 to 3,882 rows against 528 to 566 parts), so each part would be listed several times, against the README. The cost also changes: `UNION` drops a part already seen so its sub-tree is not walked again, while `UNION ALL` walks it again for every path, which grows with every level of sharing (4 levels here, more in a larger BOM). `UNION` also stops the walk if a cycle ever got through, since the rows hold the id only (no counter).
- `components_of` has no `LIMIT` (lint PERF020): the result is the complete list of parts for a declaration, and a product here has 528 to 566 of them. Any `LIMIT` returns exactly that many parts and nothing says rows are missing: with `LIMIT 100` on product 671 the declaration would drop 464 of 564 parts without an error, and a dropped part could be a restricted substance. The query is bounded already: by one product's structure, found through `uses` by `parent` (a search on the primary key in the plan). Would change if: a screen shows this result to a person; then page it in the application, but never cut a filed declaration.
- `exploded_quantities` (`UNION ALL`): it is meant to count every path ("A part that appears in three places counts three times, times the quantities"), so rows must not be merged; `qty` is multiplied down the path and summed by part number. Checked against a plain Python expansion for all 20 products: identical totals. It ends because `uses` is acyclic (README.md, confirmed in `bom.db`) and the structure is 4 levels deep; no guard is needed. A depth cap would be optional insurance only. Would change if: the PLM guarantee stops holding, because `schema.sql` only blocks self-reference (`CHECK (parent <> child)`), not longer cycles.
- `uses` primary key `(parent, child)` with `uses_child` on `(child)`: both walks go parent to child and use the primary key (the plans show a SEARCH on it); `uses_child` serves child lookups, such as where-used questions and the foreign key check when a part is deleted, though no query in `sql/` reads it. Keep it. Would change if: nothing ever looks up by child, then it only costs writes.
- `uses` stores one row per (parent, child) pair with `qty`: it is a relationship with a quantity, as it should be; `part` is the node.
- `part.substances`: stored and returned whole by `components_of`, no statement splits or matches it, and in `bom.db` every value is a single substance or NULL. Would change if: a query filters parts by substance or a part must declare several, then it needs its own table.

## Not checked
- Production size and depth of the BOM: only the 690-part copy exists here. Deeper sharing makes `UNION ALL` worse and `UNION` still right.
- The syntax for suppressing a rule in `sqlcheck`: the linter is not installed and its docs are not in the repo. Add the suppression it supports for PERF012 and PERF020 on `components_of`, with the reasons above as the comment.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
