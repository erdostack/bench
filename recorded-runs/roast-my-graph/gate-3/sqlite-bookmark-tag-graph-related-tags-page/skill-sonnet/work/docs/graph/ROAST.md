# Roast: schema.sql and queries/ (marks, SQLite)

Verdict: Two things are wrong and one of them is critical. `tag.name` is case-sensitive while every lookup is case-insensitive, so the tag page scans 450,000 tag rows to find its id and, on the sample, `/tag/python` shows only 171 of 592 bookmarks. The slowdown you saw with tag count is the scan. The rest of the design is fine.

Judged against:
- Engine: SQLite; sample checked on 3.53.1. Production version: not stated (README.md).
- Production size: about 450,000 distinct tags, 8 million bookmarks, 30 million bookmark-tag rows, largest tag about 40,000 bookmarks (README.md).
- Interactive: every tag page runs `queries/tag_id.sql`, `queries/bookmarks_for_tag.sql` and `queries/related_tags.sql`. Tag pages are case-insensitive, /tag/Python and /tag/python are the same page (README.md).
- Writers and write rate, the loader, whether foreign keys are switched on: not stated.
- Sample `marks.db`: 30,000 tags, 40,000 bookmarks, 119,906 bookmark-tag rows. 20 names exist in three spellings each (`BIRDS`, `Birds`, `birds`; `PYTHON`, `Python`, `python`).

## Findings

### critical: `tag`
The UNIQUE on `name` is the strictest bouncer in town and has never once checked what case you are wearing. `Python`, `PYTHON` and `python` all walked in as three different people.
Problem: When `/tag/python` runs `queries/tag_id.sql` on the shipped data, `name TEXT NOT NULL UNIQUE` compares bytes, so `PYTHON` (id 25), `Python` (id 28) and `python` (id 19390) are three tags. `tag_id.sql` returns only id 25 (`ORDER BY id LIMIT 1`), so `queries/bookmarks_for_tag.sql` shows 171 bookmarks where the three spellings carry 592 distinct ones, and the README says all spellings are the same page. `queries/related_tags.sql` uses all three ids, so the page disagrees with its own sidebar, and it lists the other spellings of the tag itself as related tags. The same 20 names are split this way in the sample. The binary UNIQUE index also cannot serve the case-insensitive lookup: that is the scan in the next finding.
Fix: Make the column case-insensitive so the database enforces the rule and the lookup can use the index. In SQLite 3.53.1 (tested on a copy of marks.db), merge the variants, then rebuild the table:
```sql
BEGIN;
CREATE TEMP TABLE tag_map AS
  SELECT t.id AS old_id,
         (SELECT min(m.id) FROM tag m WHERE m.name = t.name COLLATE NOCASE) AS new_id
  FROM tag t;
INSERT OR IGNORE INTO bookmark_tag(bookmark_id, tag_id)
  SELECT bt.bookmark_id, m.new_id FROM bookmark_tag bt
  JOIN tag_map m ON m.old_id = bt.tag_id WHERE m.old_id <> m.new_id;
DELETE FROM bookmark_tag WHERE tag_id IN (SELECT old_id FROM tag_map WHERE old_id <> new_id);
DELETE FROM tag WHERE id IN (SELECT old_id FROM tag_map WHERE old_id <> new_id);
CREATE TABLE tag_new (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE COLLATE NOCASE);
INSERT INTO tag_new SELECT id, name FROM tag;
DROP TABLE tag;
ALTER TABLE tag_new RENAME TO tag;
COMMIT;
```
Change `schema.sql` to the same `name TEXT NOT NULL UNIQUE COLLATE NOCASE`. On the sample this leaves 29,960 tags, id 25 carries all 592 bookmarks, and both lookups become index searches. The survivor is the lowest id, so which spelling is displayed (`PYTHON` here) is a product choice; pick it in `tag_map` if you care. NOCASE folds ASCII letters only; non-ASCII case variants stay distinct. Run with `PRAGMA foreign_keys=OFF` if your connections switch it on. Whatever code creates tags is not in these files and has to look up case-insensitively before it inserts.

### high: `queries/tag_id.sql`
Every tag page starts by reading every tag. At 450,000 tags that is a lot of reading to learn the number 19390.
Problem: When any tag page runs `WHERE name = :tag COLLATE NOCASE` against 450,000 tags, the only index on `name` is the binary UNIQUE one, so the plan is `SCAN tag` (seen on the sample) and each page reads all 450,000 rows before it can fetch a bookmark. That grows with tag count, which matches the slowdown.
Fix: The structural fix is the collation change above; after it the plan is `SEARCH tag USING COVERING INDEX sqlite_autoindex_tag_1 (name=?)` and the query can stay as written. Stopgap that keeps the case-sensitive column and still leaves the split tags: `CREATE INDEX tag_name_nocase ON tag(name COLLATE NOCASE);` (plan becomes `SEARCH`, checked on a copy).

### high: `queries/related_tags.sql`
The planner looked at "tags on the same bookmarks as :tag", shrugged, and started reading the whole bookmark_tag table.
Problem: When a tag page runs this statement, the `name = :tag COLLATE NOCASE` filter cannot use an index, and on the sample the plan is `SCAN bt USING COVERING INDEX bookmark_tag_by_tag`, checking each of the 30 million production rows against the tag lookup, on every tag page. Same cause as the `tag` finding.
Fix: The collation change above; the plan then reads `SEARCH tag ... (name=?)`, `SEARCH bt ... (tag_id=?)`, `SEARCH bt2 USING PRIMARY KEY (bookmark_id=?)` (checked after the migration on a copy). The stopgap index from the previous finding gives the same plan.

### medium: `queries/related_tags.sql`
Even with perfect indexes, the biggest tag does a few hundred thousand lookups to fill one sidebar, every time somebody looks at it.
Problem: When /tag/<largest tag> runs this statement, it joins about 40,000 bookmark-tag rows to their other tags (about 3.75 tags per bookmark in production: 30M / 8M) and sorts a GROUP BY, roughly 110,000 rows touched, on every view of that page. The answer is right but changes only when bookmarks are tagged.
Fix: Once the lookup is indexed, measure the largest tag. If it is too slow, store the top 20 per tag in a table (for example `tag_related(tag_id, other_tag_id, together)`) rebuilt by the code that writes `bookmark_tag`, or cache by tag id. Do this after the first fix, not instead of it.

## Holds up
- `queries/bookmarks_for_tag.sql`: the plan is `SEARCH bt USING COVERING INDEX bookmark_tag_by_tag (tag_id=?)` then a primary-key lookup on `bookmark`, with no sort step because the index order is the ORDER BY. LIMIT 50 stops it early, so the 40,000-bookmark tag costs 50 rows. It is only wrong when handed the wrong id (see `tag`).
- `bookmark_tag_by_tag`: the primary key leads with `bookmark_id`, so a lookup by tag needs an index leading with `tag_id`. This one is used by both queries; it is not redundant.
- `bookmark_tag`: a plain many-to-many link. Only `tag` and `bookmark` touch it and it carries no properties of its own, which is what a link table in SQL is. Its `tag_id` and `bookmark_id` are covered by the index and the primary key, so no index is missing.
- `bookmark.user_id`: nothing in the files filters on it, so no index is needed for what is shown.

## Not checked
- Speed at production size: the sample (30,000 tags) shows plan shape and result correctness, not timings.
- The production SQLite version, and how tags are created and attached: no loader or application code in the repo, so I could not confirm where the case variants come from or whether `PRAGMA foreign_keys` is on.
- The migration was run on an in-memory copy of `marks.db`, not on production data. Back up first.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
