# Roast: citegraph (schema.sql, import_refs.py, export_edges.py, ranking/, queries/)

Verdict: the odd syllabus ranking is the import, not the papers. The foreign key on `cites` was never enforced, so 15,708 citations to papers outside the corpus are stored and rank first.

Judged against: ~12,000 papers (README.md; 12,000 rows in `paper`); `cites.db` and `data/refs.csv` are this term's import (README.md); references to papers outside the corpus are supposed to be skipped via `cites.cited_id` REFERENCES `paper(id)` (README.md); `export_edges.py` feeds `ranking/rank.py` for the syllabus (README.md); engine: SQLite 3.53.1 as run here, version of the user's install not stated; write rate: one import per term, batch.

## Findings

### critical: `load`
A foreign key that is a stern suggestion. SQLite shipped it with the safety off and nobody turned it on.
Problem: When `load` in `import_refs.py` runs on `data/refs.csv`, it opens a connection without `PRAGMA foreign_keys = ON` (nothing in the repo sets it), so the `REFERENCES paper(id)` on `cites.cited_id` is not checked. In `cites.db` 15,708 of 66,059 rows point at 1,493 ids not in `paper`; only 101 repeated pairs were skipped, so the importer reports 99.8% resolved where the real figure is 50,351 of 66,160 (76.1%).
Fix: `con.execute("PRAGMA foreign_keys = ON")` after connect; count unresolved (id not in a set from `SELECT id FROM paper`) and duplicate (primary key) rejections separately. Migrate: `DELETE FROM cites WHERE cited_id NOT IN (SELECT id FROM paper);`, re-run `export_edges.py` and `ranking/rank.py`; `PRAGMA foreign_key_check` must return nothing.

### high: `main`
PageRank, now with ghosts.
Problem: When `main` in `ranking/rank.py` ranks `edges.tsv` built from the shipped `cites`, 1,493 of its 13,493 nodes are not papers and all of the top 25 are such ids (414727, 640823, 881501, 536099, 876276 ...), printed with title "?". On the 12,000 real papers the top is 205763, 176687, 312376.
Fix: clean the data first (above); then drop ids absent from `titles` before `nx.pagerank` and fail loudly if any were found.

### medium: `main`
Problem: `main` in `export_edges.py` exports every `cites` row without checking both ends exist in `paper`, passing the dangling edges to the ranking.
Fix: `SELECT c.citing_id, c.cited_id FROM cites c JOIN paper a ON a.id = c.citing_id JOIN paper b ON b.id = c.cited_id ORDER BY c.citing_id, c.cited_id`.

### low: `reference_list.sql`
Problem: the LEFT JOIN on `paper` exists only to survive cited ids with no paper; on the shipped data it returns NULL title and year rows that sort first on the paper page.
Fix: after the cleanup, use `JOIN paper p ON p.id = c.cited_id` and select `p.id`.

### low: `load`
Problem: one commit per CSV row (66,160 transactions); slow, finishes, rare batch job.
Fix: optional, one transaction around the loop.

## Holds up
- `cites`: WITHOUT ROWID keyed by `(citing_id, cited_id)` plus `cites_by_cited` makes both directions index searches (EXPLAIN QUERY PLAN: SEARCH on each); the CHECK on self-citation matches the data (0 self-citations in `data/refs.csv`).
- `most_cited.sql`: the inner join to `paper` already drops ghost ids, so it is right on this data.
- `cited_by.sql`: covering index search, correct.

## Not checked
- Ran read-only on the shipped `cites.db`; PageRank was run with NetworkX 3.7 on the shipped edges, not through `edges.tsv`. The user's SQLite version was not stated.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
