# Roast: tinywiki storage (schema.sql, wikistore/, scripts/, wiki.db staging copy)

Verdict: Not sound. The schema declares `ON DELETE CASCADE` on both ends of `link`, the README and `delete_page` promise that deleted pages vanish from the backlinks panel and the "Popular pages" sidebar, and none of it happens: `open_store` never turns foreign keys on, so SQLite ignores every `REFERENCES` clause. The staging copy shows the result: 2,576 of 8,220 `link` rows point at pages that no longer exist, "Popular pages" counts them (the top page shows 66 inbound links, the real number is 20), and the next page created inherits links meant for a deleted one. The fix is one line plus a one-off cleanup.

Judged against:
- Engine: SQLite; library version of this machine's Python `sqlite3` is 3.53.1 (run). Production version: not stated.
- Size: about 40,000 pages and 600,000 links in production (README.md). The staging copy `wiki.db` has 1,440 pages, 8,220 links, 7 banned accounts.
- Writers: `wikistore/store.py` is the only code that touches the database; handlers call `open_store()` once per request (README.md). `scripts/spam_sweep.py` runs every night and last month removed about 900 pages (README.md).
- Stated guarantee: "Deleting a page removes its links in both directions ... so the backlinks panel and the 'Popular pages' sidebar never count a deleted page" (README.md; same claim in the `delete_page` docstring).
- Read paths and how often the sidebar and panel render: not stated.

## Findings

### critical: `open_store`
A foreign key with `ON DELETE CASCADE` and no `PRAGMA foreign_keys = ON` is a very detailed wish. SQLite reads the wish, files it, and deletes the page anyway. The graveyard is 2,576 links deep and the sidebar is taking attendance of the dead.
Problem: When `delete_page` (called by `scripts/spam_sweep.py` for about 900 pages a month) runs `DELETE FROM page`, the cascades declared on `link.src` and `link.dst` in schema.sql do not fire, because `open_store` opens the connection without `PRAGMA foreign_keys = ON` and SQLite leaves foreign keys off on every new connection (PRAGMA foreign_keys returned 0 on `wiki.db`; no file enables it). On the staging copy this has already left 2,576 orphan rows in `link` (1,386 with a missing `src`, 1,190 with a missing `dst`; `PRAGMA foreign_key_check` lists 2,576), all pointing at ids 1441 to 1540 of deleted pages, and the README guarantee does not hold.
Fix: Turn the pragma on for every connection, right after connecting and before any transaction: in `open_store` add `con.execute("PRAGMA foreign_keys = ON")` before `return con`. Then clean the existing orphans, once, on staging and production after a backup: `DELETE FROM link WHERE src NOT IN (SELECT id FROM page) OR dst NOT IN (SELECT id FROM page);` and confirm that `PRAGMA foreign_key_check;` returns no rows. Tried on a copy of `wiki.db`: 8,220 rows became 6,497, foreign_key_check was empty, and deleting a heavily linked page afterwards removed its links in both directions. Cascades on `dst` use the `link_by_dst` index and cascades on `src` the primary key, so each delete stays cheap.

### high: `most_linked`
A popularity contest where the dead still vote, and where one ghost-stuffed page ("Budget oncall notes 2") wins with 66 votes it earned 20 of.
Problem: When the sidebar calls `most_linked`, it joins `link` to `page` on `l.dst` only, so links coming from deleted pages are counted. On the staging copy the query returns "Budget oncall notes 2" 66, "Payments mobile notes 4" 66, "Budget release notes 1" 60 at the top; counting only links whose `src` is a live page gives "Payments mobile notes 4" 25, "Auth deploy notes 0" 20, "Budget release notes 1" 20, "Budget oncall notes 2" 20. Both the numbers and the order shown to users are wrong, and 45 pages have an inflated count.
Fix: Fix the cause (see `open_store`: pragma plus orphan cleanup); after that the query is correct as written. Until that is deployed, a labelled stopgap: add `JOIN page s ON s.id = l.src` to the statement.

### high: `backlinks`
Create a page and it moves into the dead page's old apartment, mailbox still full.
Problem: `page.id` is `INTEGER PRIMARY KEY` without `AUTOINCREMENT`, so SQLite hands out the largest existing id plus one. Staging has page ids 1 to 1440 and orphan links to ids 1441 to 1540, so the next new page gets id 1441 and `backlinks` for it returns pages that linked to the deleted page that used to have that id. Run on a copy of `wiki.db`: `save_page(con, 'brand-new', 'Brand new', 'hello', 'user001')` returned id 1441 and `backlinks(con, 'brand-new')` listed 4 pages (`team-update-1`, `team-update-25`, `team-update-35`, `team-update-38`) that never linked to it. The same applies to every deleted page whose id is at the top of the range.
Fix: Same cause as `open_store`: with foreign keys on and the orphans deleted, no `link` row can refer to a reused id, so no schema change is needed. Do not switch to `AUTOINCREMENT` as the fix; it would hide the symptom while leaving the orphans in place.

### low: `save_page`
Question to confirm, not a defect: a `[[slug]]` to a page that does not exist yet is silently dropped (`INSERT OR IGNORE ... SELECT ?, id FROM page WHERE slug = ?` inserts nothing), and nothing adds the link when the target page is created later, so its backlinks panel stays empty until the source page is saved again. The README says links are rebuilt on every save and does not say whether a link to a page that does not exist yet should appear once it does. If it should, store the target slug in `link` (or create the links for pages whose body mentions the new slug in `save_page` when a page is created); if not, nothing to change. Staging bodies contain no `[[...]]` text, so I could not check how often this happens.

## Holds up
- `link_by_dst`: `(dst, src)` serves `backlinks` and the `ON DELETE CASCADE` lookups on `dst`; the primary key `(src, dst)` serves `src`. Neither duplicates the other, so both are needed. `link` as a pure two-sided relation with no extra properties is right: nothing else refers to a link.
- `spam_sweep.py`: the lookup `created_by IN (SELECT username FROM banned_account)` scans `page` (no index on `created_by`), once a night over about 40,000 rows. A scan in a nightly batch is right at that size. Deleting page by page in separate transactions is fine for about 900 pages.
- `lonely_pages`: `id NOT IN (SELECT dst FROM link)` is safe because `link.dst` is `NOT NULL`. On the staging copy it returns the same 20 pages with and without the orphan rows; it will be right once the orphans are gone.
- `save_page`: one transaction per save, upsert keyed on the unique `slug`, `DELETE` then `INSERT` of the outgoing links, deduplicated by `set()` and the primary key. Sound for the stated workload.
- `page` / `slug`: `UNIQUE` on `slug` gives the index the lookups by slug use.

## Not checked
- Production: only the staging copy `wiki.db` was read (read-only, on a copy in a temporary file). The production orphan count is not known; the README numbers say it should be at least as bad.
- How often the sidebar and backlinks panel render: not stated. `most_linked` reads every `link` row to count them (600,000 in production), so if it runs on every page view, caching or a stored count is worth asking about once the counts are right.
- The SQLite version in production, and whether any other process opens `wiki.db` without going through `open_store`.
- Staging page bodies contain no `[[slug]]` text, so consistency between page bodies and `link` rows could not be checked.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
