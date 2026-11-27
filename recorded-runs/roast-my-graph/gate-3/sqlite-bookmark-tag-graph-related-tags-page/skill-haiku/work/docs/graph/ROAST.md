# Roast: marks schema.sql and queries/

Verdict: Not nothing serious. The tag pages are slow for a fixable reason: the tag lookup cannot use its index, because the query asks for NOCASE and the index is BINARY. They are also wrong for a worse reason: each tag is stored under up to three casings, and the page shows only one of them. Fix the duplicate tags first, then add the NOCASE index.

Judged against:
- README: about 450,000 distinct tags, 8 million bookmarks, 30 million bookmark-tag rows, largest tag about 40,000 bookmarks; marks.db is a sample (README.md).
- README: tag pages are case-insensitive, /tag/Python and /tag/python show the same page; related tags box on every tag page (README.md).
- README: bookmarks_for_tag lists the newest bookmarks by id, exact match, and the API resolves the id first (README.md, queries/tag_id.sql).

## Findings

### critical: `tag.name`
Three spellings of birds walk into a UNIQUE constraint. It checks the bytes, the README checks the vibes, and the tag page picks whichever one has the lowest id and shrugs.
Problem: On marks.db, 30,000 tag rows hold only 29,960 distinct lower-cased names. 20 names appear under three spellings (BIRDS id 1 with 188 bookmarks, Birds id 2 with 181, birds id 41 with 176). tag_id.sql returns only the lowest id, so /tag/birds lists id 1's bookmarks alone. The README says these must be one page.
Fix: One migration in one transaction: map each tag to MIN(id) over lower(name); INSERT OR IGNORE the bookmark_tag rows onto the canonical id; DELETE the bookmark_tag and tag rows of the other ids; then CREATE UNIQUE INDEX tag_name_nocase ON tag(name COLLATE NOCASE). Tested on a copy: tags 30,000 to 29,960, bookmark_tag 119,906 to 119,860, and birds has 543 bookmarks on id 1. The index fails if created before the merge. Not run on production; back up and rehearse first.

### high: `queries/tag_id.sql`
The lookup reads every tag row to find one tag. That is a linear scan with a very confident index sitting next to it, unused.
Problem: `name = :tag COLLATE NOCASE` cannot use the UNIQUE index on tag.name, which is BINARY. EXPLAIN QUERY PLAN on marks.db shows SCAN tag. At 450,000 tags, every tag page reads every tag row, so the cost grows with tag count. The page is hot and the table is large.
Fix: After the merge under tag.name, run CREATE UNIQUE INDEX tag_name_nocase ON tag(name COLLATE NOCASE); (or declare name TEXT NOT NULL UNIQUE COLLATE NOCASE when the table is rebuilt). The plan becomes SEARCH tag USING COVERING INDEX tag_name_nocase (name=?). Verified on SQLite 3.53.1 only.

### high: `queries/related_tags.sql`
The related-tags box asks for two tags' worth of rows and gets the whole link table, which is the query equivalent of ordering a sandwich and being handed the bakery.
Problem: EXPLAIN QUERY PLAN shows SCAN bt USING COVERING INDEX bookmark_tag_by_tag. The CTE t is not used to seek the index, so every related-tags request reads the whole link table. At the README's 30 million rows, that happens on every tag page view. The plan shape comes from the 120,000-row sample; production was not run.
Fix: Bind the tag id with a scalar subquery so the join seeks: FROM tag t JOIN bookmark_tag bt ON bt.tag_id = t.id ... WHERE t.id = (SELECT id FROM tag WHERE name = :tag COLLATE NOCASE). With the NOCASE index, the plan becomes SEARCH bt USING COVERING INDEX bookmark_tag_by_tag (tag_id=?). Apply after the tag.name migration, so the subquery returns one id.

### low: `queries/bookmarks_for_tag.sql`
Problem: The query orders by bookmark id, which the README calls newest. bookmark.saved_at is never used for ordering. If saved_at order was meant, the current index does not serve it. This is a question to confirm, not a defect.
Fix: None if id order is intended. If saved_at order is intended, confirm first; it would need its own index.

## Holds up
- `bookmark_tag_by_tag` (tag_id, bookmark_id): leads with tag_id, so bookmarks_for_tag.sql seeks by tag and reads in bookmark_id order with no temp sort in the plan. Would change if the query filtered by bookmark_id alone, which it does not.
- `bookmark_tag` PRIMARY KEY (bookmark_id, tag_id) WITHOUT ROWID: serves the co-tag self-join in related_tags.sql (SEARCH bt2 USING PRIMARY KEY). Would change if a query needed to find a bookmark's tags by tag alone.
- `bookmark_tag` as a link table: a many-to-many between bookmark and tag with no properties of its own. That is the normal shape here; nothing to collapse.
- `bookmark` primary key: the join in bookmarks_for_tag.sql seeks by rowid.

## Not checked
- Production plans and timings: only the 120,000-row sample was run. The 30-million-row plan shape is inferred from the sample plan.
- The migration was tested on a copy of marks.db only, not on production and not timed.
- Index syntax verified on SQLite 3.53.1 only.
- Runtime was not measured, only plans. The GROUP BY cost in related_tags.sql for a 40,000-bookmark tag is not measured.
- The API code is not in the repo; the id-first resolution is taken from the README.
- schema.sql and queries/ were not edited.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
