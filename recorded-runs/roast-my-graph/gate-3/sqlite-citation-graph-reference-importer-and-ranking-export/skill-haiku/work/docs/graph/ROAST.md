# Roast: citegraph (schema.sql, import_refs.py, export_edges.py, ranking/, queries/)

Verdict: Not just the papers. Nothing is wrong with the papers. The problem is that `cites` accepts citations to papers that are not in the corpus. 15,708 of the 66,059 stored rows point at 1,493 ids that have no row in `paper`, and those ids are exactly the top 25 of the syllabus ranking. The README says these rows are skipped; they are stored, because the foreign key is never switched on.

Judged against:
- Corpus is about 12,000 papers (`README.md`; `paper` holds 12,000 rows in `cites.db`).
- One term's import of 66,160 reference rows (`data/refs.csv`, 101 of them repeated pairs). Loaded in batch, once per term (`README.md`).
- `ranking/rank.py` ranks papers for the syllabus (`README.md`). `queries/` back the paper page, which is interactive (`README.md`, `queries/reference_list.sql`, `queries/cited_by.sql`).
- Stated invariant: "both must be papers in the corpus" (`schema.sql`, comment above `cites`). Stated behaviour: out-of-corpus references "are skipped" and the importer "prints the coverage" (`README.md`).
- Engine: SQLite through Python's `sqlite3`. The version is not stated in the repo. Checked here with SQLite 3.53.1.

## Findings

### critical: `cites`
Problem: When `INSERT INTO cites` runs against a cited_id that is not in `paper`, the row is stored, because `PRAGMA foreign_keys` is off on a new connection and nothing in `import_refs.py`, `export_edges.py` or `ranking/rank.py` turns it on. In `cites.db`, `PRAGMA foreign_key_check(cites)` returns 15,708 rows. The top 25 PageRank nodes that `ranking/rank.py` prints are all ids missing from `paper`, so every one prints `?` as its title.
Fix: Run `PRAGMA foreign_keys = ON` right after each `sqlite3.connect` (`import_refs.py` `main`, `export_edges.py` `main`, `ranking/rank.py` `main`). Migration on the stored file: run `PRAGMA foreign_key_check(cites)`, move the 15,708 flagged rows to a `cites_unresolved` table or delete them, then re-import. Tested on an in-memory copy with SQLite 3.53.1: with the pragma on, the import loads 50,351 rows and leaves 0 foreign key violations.

### high: `load`
Problem: The `except sqlite3.IntegrityError` branch in `load` counts a repeated pair (a PRIMARY KEY failure) and an out-of-corpus cited paper (a foreign key failure) as the same "skipped". Because the foreign key is never enforced, the printed coverage in the stored run is wrong: the importer reports resolved 66059 of 66160 (99.8%) when only 50,351 of 66,160 (76.1%) are actually in the corpus. Running the importer again on the same CSV reports `resolved 0 of 66160 (0.0%)`.
Fix: Set the pragma as in the `cites` fix. Insert with `INSERT OR IGNORE` and test `cursor.rowcount`: 0 means a repeated pair. A foreign key failure still raises `IntegrityError` and is counted as not in the corpus. Tested with SQLite 3.53.1: a repeat pair returns rowcount 0, and an out-of-corpus cited id raises `FOREIGN KEY constraint failed`.

### low: `reference_list.sql`
Problem: This file LEFT JOINs `paper` and orders by `p.year`. In SQLite, NULL years sort first, so the paper page for citing id 116129 lists four unresolved references with no title at the top. This only shows up while the stored orphans exist. If the intent is to show unresolved references, they should go last; if not, the JOIN should be inner.
Fix: After the `cites` migration, change `LEFT JOIN` to `JOIN`. If unresolved references should stay, use `ORDER BY p.year IS NULL, p.year`. Confirm which intent is meant before choosing.

## Holds up
- `cites` primary key `(citing_id, cited_id)` with `WITHOUT ROWID`: repeated pairs are rejected, and `queries/reference_list.sql` finds by `citing_id` through `SEARCH c USING PRIMARY KEY (citing_id=?)`.
- `cites_by_cited` `(cited_id, citing_id)`: `queries/cited_by.sql` runs `SEARCH c USING COVERING INDEX cites_by_cited (cited_id=?)`, so the lookup does not scan.
- `CHECK (citing_id <> cited_id)` on `cites`: 0 self-citations in the stored data or the CSV.
- `queries/most_cited.sql`: it JOINs `paper` on `cited_id`, so out-of-corpus ids are left out of its output. It scans `paper` once (12,000 rows), which is cheap at this size.
- `ranking/rank.py` edge direction (citing to cited, read by `nx.read_edgelist`): PageRank gives credit to the cited paper, as citation ranking should. The bad output comes from the stored ids, not from this direction.

## Not checked
- The `export_edges.py` and `ranking/rank.py` scripts were not run as shipped, because they write `edges.tsv` into the working directory. Their logic was reproduced in memory on a copy of `cites.db`, which was opened read-only and not changed.
- The `load` fix was tested in memory, not on `cites.db`. The migration was not applied.
- Timing of the importer: it commits once per row (66,160 commits). Not timed.
- The CSV's cited ids outside the corpus may be real papers missing from `paper`, which is a corpus gap, not an importer bug. This review cannot tell the two apart.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
