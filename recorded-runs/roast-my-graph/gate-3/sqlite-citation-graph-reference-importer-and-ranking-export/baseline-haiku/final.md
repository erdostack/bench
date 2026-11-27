The odd syllabus ranking is not just the papers. The import is leaking references into the graph.

**What's wrong**

1. **Foreign keys are never enforced.** `import_refs.py` never sets `PRAGMA foreign_keys = ON`, so SQLite accepts `cites` rows whose `cited_id` is not in `paper`. 15,708 of 66,059 rows (23.8%) are like this. The `IntegrityError` branch only catches the 101 duplicate pairs. The README says out-of-corpus references get rejected, which is not what happens. The printed "resolved 66059 of 66160 (99.8%)" is wrong. The real coverage is 50,351 of 66,059 distinct references (76.2%).
2. **The ranking is dominated by out-of-corpus IDs.** `export_edges.py` writes every `cites` row. The 1,493 missing papers become sink nodes in the PageRank graph and absorb about 20% of the mass. All of the top 25 in `ranking/rank.py` are non-corpus IDs with title `?`. That is the odd syllabus list.
3. **Citation direction or years look wrong.** In 24,712 joined rows (37.4%), the citing paper is older than the cited paper. A citation normally points backwards in time, so either the `citing_id`/`cited_id` columns are swapped for some rows or the `paper.year` values are off. Check this before trusting any ranking.
4. **Duplicate papers.** 1,986 titles appear under more than one `paper.id` (one title has 15 ids). This splits citation counts.
5. Smaller items: `queries/reference_list.sql` shows blank title and year rows (NULLs sort first) for out-of-corpus references, and `import_refs.py` commits once per row, so the import is slow and not atomic.

**Fixes, in order**

- Set `PRAGMA foreign_keys = ON` in `import_refs.py` `main()`, or check paper membership in `load()`, and make the coverage line and README match the real numbers.
- Filter `export_edges.py` to in-corpus `cited_id` values (join to `paper`), then re-run the ranking. Expect a very different top 25.
- Check the direction and year source in the reference manager export on a sample, then reload.
- Dedupe titles under a stable key such as a DOI before adding a UNIQUE constraint.

All eight findings, with element names and fixes, are in `findings.json` in the repo root. I did not change any code or the database. I regenerated `edges.tsv` only to test the ranking and then deleted it.
