Tag pages slow down as the tag count grows for one main reason: the tag lookup cannot use an index. Findings are also in `findings.json` in the repo root.

**Critical: the tag lookup scans the whole `tag` table.** `tag.name` is `UNIQUE` with the default BINARY collation, but `tag_id.sql` and `related_tags.sql` both match with `COLLATE NOCASE`. The unique index cannot serve that, so `EXPLAIN QUERY PLAN` shows `SCAN tag`. Fix: `CREATE INDEX tag_name_nocase ON tag(name COLLATE NOCASE);`. On an in-memory copy of `marks.db` the plan becomes an index search.

**High: the tag page shows only part of the tag.** `tag_id.sql` uses `ORDER BY id LIMIT 1`, so /tag/python resolves to one of three case variants (ids 25, 28, 19390). Id 25 has 171 bookmarks, and 592 distinct bookmarks carry some variant. `bookmarks_for_tag.sql` filters on that one id, so the newest-50 list misses bookmarks on the other variants. Fix: resolve to all matching ids and filter with `tag_id IN (SELECT id FROM tag WHERE name = :tag COLLATE NOCASE)`. I checked that this returns 50 rows through the index in about 1 ms on the sample.

**High: related tags re-aggregates on every page view.** Even with the index, `related_tags.sql` groups every bookmark on the tag each time. On the largest production tag (about 40,000 bookmarks) that is on the order of 150,000 join rows per request. The rewrite above drives the join from the index and cut the sample run from about 14 ms to about 1.4 ms (one run each, so indicative only). For production, precompute a co-occurrence table per canonical tag, or cache per tag with a TTL. The query also lists case variants of other tags as separate entries, so 'python' and 'Python' can both appear in the box.

**High: 20 case-duplicate groups in `tag`.** Examples are 'PYTHON', 'Python' and 'python'. The case-sensitive UNIQUE allows them, and they are the root of the two correctness issues above. Fix: store a canonical case-folded name or declare `COLLATE NOCASE` on the UNIQUE column. Migrate first by moving `bookmark_tag` rows to the surviving id with `INSERT OR IGNORE`, then deleting the emptied tags, inside a transaction, with a backup.

**Low: orphaned tags.** 777 of 30,000 tags have no bookmarks and nothing removes them. Clean them up on bookmark delete or periodically, after the dedupe migration.

I did not change `schema.sql` or the queries, and I did not modify `marks.db`. All timings are single runs on the small sample.
