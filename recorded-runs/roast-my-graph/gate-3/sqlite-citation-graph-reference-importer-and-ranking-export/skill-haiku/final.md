Not just the papers. The ranking is odd because `cites` stores citations to papers that are not in the corpus. 15,708 of the 66,059 stored rows point at 1,493 ids with no row in `paper`, and the top 25 of the syllabus ranking are all of those ids, printed as `?`.

The cause is that `PRAGMA foreign_keys` is never switched on, so the `REFERENCES paper(id)` clause does nothing. The README says these references are skipped; they are stored. The importer's coverage line is also wrong: it reports 99.8%, and the real figure is 50,351 of 66,160 (76.1%).

Findings, worst first:
- critical, `cites`: enable foreign keys on every connection, then move or delete the flagged rows and re-import. Tested in memory: the import then loads 50,351 rows with 0 violations.
- high, `load` in `import_refs.py`: duplicates and out-of-corpus papers are both counted as "skipped". Use `INSERT OR IGNORE` and check `rowcount`.
- low, `queries/reference_list.sql`: unresolved references sort first on the paper page.

The three queries and the `cites_by_cited` index hold up.

Review: `/run/work/docs/graph/ROAST.md`. Findings: `/run/work/findings.json`.
