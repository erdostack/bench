Not nothing serious. The tag pages are slow because the tag lookup cannot use its index: the query asks for `COLLATE NOCASE` and the UNIQUE index on `tag.name` is BINARY, so `queries/tag_id.sql` scans the tag table. The pages are also wrong: each tag is stored under up to three casings and the page shows only one of them (on marks.db, /tag/birds shows 188 of 545 bookmarks).

Top findings:
1. critical, `tag.name`: duplicate casings. Merge onto the lowest id per lower(name), then add `CREATE UNIQUE INDEX tag_name_nocase ON tag(name COLLATE NOCASE)`. Tested on a copy only.
2. high, `queries/tag_id.sql`: the lookup scans all tags. The NOCASE index above turns it into a search.
3. high, `queries/related_tags.sql`: the plan scans the whole bookmark_tag table on every tag page. Binding the tag id with a scalar subquery makes it seek.
4. low, `queries/bookmarks_for_tag.sql`: "newest" means bookmark id order; confirm that is the intent.

Full roast: /run/work/docs/graph/ROAST.md
Findings list: /run/work/findings.json

Not run: production plans and timings (only the 120k-row sample), and the migration has not been run on production data.
