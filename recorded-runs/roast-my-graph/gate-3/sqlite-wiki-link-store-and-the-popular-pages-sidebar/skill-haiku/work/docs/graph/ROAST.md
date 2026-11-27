# Roast: tinywiki storage (schema.sql, wikistore/, scripts/)

Verdict: Not sound. Deleting a page does not remove its links, because nothing in the code switches foreign keys on, so the schema's `ON DELETE CASCADE` never runs. The staging copy already has 2,576 dangling link rows, the "Popular pages" counts include links from deleted pages, and the nightly sweep adds more every night. Separately, `save_page` drops links to pages that do not exist yet. The fix for the first is small; the cleanup needs a migration.

Judged against:
- Engine: SQLite 3.53.1 (run here). The repo does not state a version.
- Size: production about 40,000 pages and 600,000 links (README.md). wiki.db is a staging copy with 1,440 pages and 8,220 links (counted from the file).
- Interactive paths: the backlinks panel, the "Popular pages" sidebar, and page saves (README.md, wikistore/store.py). How often the sidebar renders: not stated.
- Batch path: scripts/spam_sweep.py, nightly. It removed about 900 pages last month (README.md).
- Writers: save_page and delete_page in wikistore/store.py, plus the nightly sweep.
- Stated guarantee: deleting a page removes its links in both directions via `ON DELETE CASCADE`, so the backlinks panel and the sidebar never count a deleted page (README.md; the docstring of delete_page repeats it).
- Stated rule: `save_page` rebuilds a page's outgoing links on every save (README.md).
- Staging bodies: all 1,440 `body` values are empty, so the link table cannot be checked against the `[[slug]]` text.

## Findings

### critical: `link`
The cascade you were promised is a pragma away, and the code never sets it.
Problem: SQLite leaves foreign keys off on every new connection, and `open_store` never runs `PRAGMA foreign_keys = ON`. A read-only connection to wiki.db reports 0. So `delete_page` removes only the page row. On the staging copy, `PRAGMA foreign_key_check` reports 2,576 violations: 1,386 link rows whose `src` is gone and 1,190 whose `dst` is gone. In an in-memory copy, deleting one page left all 8,220 links in place and added 14 orphan `src` rows, which are that page's outgoing links. The effects are visible. On staging the sidebar shows "Budget oncall notes 2" with 66 inbound links, and 20 of them come from live pages. A page recreated after its old id was the highest id gets that id again, since the table has no AUTOINCREMENT, and it inherits 10 stale incoming links. The sweep runs nightly and removes about 900 pages a month, so the orphans grow every night.
Fix: Make the write path explicit so it does not depend on a pragma. In `delete_page`, run `DELETE FROM link WHERE src = ? OR dst = ?` in the same transaction as the page delete. Also add `con.execute("PRAGMA foreign_keys = ON")` in `open_store`, before any transaction starts, so the declared constraint is enforced. Then run a one-off migration after the nightly sweep is paused: `DELETE FROM link WHERE src NOT IN (SELECT id FROM page) OR dst NOT IN (SELECT id FROM page)`. Confirm `PRAGMA foreign_key_check` returns no rows afterwards. The id reuse goes away once the orphans do.

### high: `save_page`
Problem: `INSERT OR IGNORE INTO link (src, dst) SELECT ?, id FROM page WHERE slug = ?` inserts nothing when the target slug has no page yet. In an in-memory copy, a page that linked to a missing slug recorded 0 links. After the target page was created, its backlinks were empty, and the link appeared only after the linking page was saved again. Nothing in the files shows this being intended. The shipped bodies are empty, so this is not visible in the data, only in the code path.
Fix: Record the target slug when the page does not exist yet. Add a table such as `pending_link (src INTEGER NOT NULL REFERENCES page(id) ON DELETE CASCADE, dst_slug TEXT NOT NULL, PRIMARY KEY (src, dst_slug))`. In `save_page`, insert into it for the slugs that do not resolve. When a page is created, move its matching `pending_link` rows into `link` in the same transaction. Test it first: save a page with a red link, create the target, and assert the backlink is there.

### medium: `most_linked`
Problem: The sidebar query scans every link row on each call. The plan is `SCAN l USING COVERING INDEX link_by_dst` followed by a temp B-tree for the sort. That is 8,220 rows on staging and about 600,000 in production. The README does not say how often the sidebar renders. If it is drawn on each page view, as the per-request store suggests, each view scans the whole link table.
Fix: Keep a counter on the page. Add `inbound INTEGER NOT NULL DEFAULT 0` to `page` with an index on it, and change `save_page` and `delete_page` to update it in the same transaction as the link rows. Then `most_linked` becomes `SELECT title, inbound FROM page ORDER BY inbound DESC LIMIT ?`. Do this after the link fix, or the counter inherits the orphans.

## Holds up
- `backlinks`: the plan is `SEARCH l USING COVERING INDEX link_by_dst (dst=?)`. The index `link_by_dst (dst, src)` leads with the filtered column, which is what the panel needs. Orphan `src` rows are excluded by the join to `page`, so the panel is right except for the id reuse above.
- `link` primary key `(src, dst)` with `WITHOUT ROWID`: serves lookups by `src` (the save path's DELETE). Together with `link_by_dst`, both directions are indexed. No change needed.
- `lonely_pages`: a full scan of `page` with `link_by_dst` for the `NOT IN` check. It is the gardening report, a rare batch, so the scan is fine. It returned 20 on both the stored and the live-only links on staging, so orphans do not change its answer there.
- `scripts/spam_sweep.py`: the `created_by IN (SELECT username FROM banned_account)` lookup scans `page`, which is fine for a nightly batch at 1,440 rows here and about 40,000 in production. Each delete commits separately; a crash leaves a partial sweep, which the next run finishes. The sweep is correct as written once the link fix is in.
- `save_page` upsert: `ON CONFLICT (slug)` keys on the slug, which is UNIQUE and is the page's permanent address. Title and body change without changing the key.

## Not checked
- Production data was not available. wiki.db is staging, and the production figures are from the README.
- The staging `body` values are all empty, so the link table could not be compared with the `[[slug]]` text.
- Nothing was written to wiki.db. The read-only checks used a `mode=ro` connection, and the deletes and saves were run on an in-memory copy through wikistore/store.py.
- `PRAGMA foreign_keys = ON` and the cleanup migration were not run, so their behaviour is from the SQLite documentation for this version, not from a run here.
- The nightly sweep was not run. `delete_page` was called directly.
- The id reuse was observed on the in-memory copy with SQLite 3.53.1. The `AUTOINCREMENT` alternative was not tested.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
