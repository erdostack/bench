Don't apply either linter suggestion. Both are false positives for `components_of`, and applying them would make the compliance declaration wrong.

**PERF012, UNION to UNION ALL.** The UNION is doing a job. Sub-assemblies are shared, so the same part is reached by many paths, and `components_of` has to list each part once for the customs and REACH declarations. UNION removes those repeats and also stops the recursion from re-expanding a shared sub-assembly for every path. I ran both versions against `bom.db`. For product 671 the original returns 564 rows and the UNION ALL version returns 3,604. The other products I tried were about six times larger in the same way. The declaration would list parts several times, and run time would grow with depth and sharing.

**PERF020, add a LIMIT.** This is worse, because it fails silently. The result is a complete declaration, not a page of results. Products in `bom.db` contain 528 to 564 parts. A LIMIT below that drops parts, along with their restricted substances, and the query still looks successful. The output is bounded by the size of one product, so there is nothing to protect against.

Instead, suppress both warnings for `components_of` with your linter's suppression syntax and note the reason next to the suppression. I don't know sqlcheck's exact syntax, so I did not edit the lint file.

**Rest of `sql/`** (7 entries in `findings.json`, none critical):
- **medium, `exploded_quantities`:** UNION ALL is correct there, because quantities must multiply along every path. But it has no cycle guard or depth bound, so a cyclic export would hang it. Add a depth limit. It runs in about 8 ms per product now, but it enumerates every path and can grow sharply as nesting gets deeper.
- **medium, `part.substances`:** 316 of 690 parts have NULL, and a missing declaration looks the same as "none declared". Decide what NULL means, or move substances to their own table with one row each.
- **low, `components_of`:** the query is correct. A product id that doesn't exist, or isn't a product, returns an empty list that looks like a valid declaration. Check it in the caller.
- **low, `uses`:** SQLite does not enforce the foreign keys unless `PRAGMA foreign_keys = ON` is set. Nothing stops a component having children. The current data is clean, and I found no cycles or dangling ids. Acyclicity comes only from the PLM system. Validate on load.
- **low, `uses_child`:** no query uses this index. Keep it if you plan where-used lookups, and add the query.
- **high, `lint/findings.txt`:** two entries, one per warning, so they can be tracked as "do not apply".
