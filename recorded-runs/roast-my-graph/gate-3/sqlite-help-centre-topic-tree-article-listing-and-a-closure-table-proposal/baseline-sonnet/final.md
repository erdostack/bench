**No, a closure table is not warranted. The review's claim is wrong.**

SQLite can use an index for `LIKE 'prefix%'` when the column's collation is case-insensitive, and `topic.path` is `UNIQUE COLLATE NOCASE`. I ran `EXPLAIN QUERY PLAN` on `kb.db` (SQLite 3.53.1):

- `subtree_articles.sql`: `SEARCH t USING COVERING INDEX sqlite_autoindex_topic_1 (path>? AND path<?)`, then `SEARCH a USING INDEX article_topic (topic_id=?)`.
- `move_topic.sql`: `SEARCH topic USING INDEX sqlite_autoindex_topic_1 (path>? AND path<?)`.

Neither query scans the table. Both are range seeks on the unique path index, so cost follows subtree size, not the 400k topic count. A topic page on the 40k sample takes about 1 ms. Moves are rare and use the same index. A closure table would add a trigger-maintained table with a row for every ancestor/descendant pair, in exchange for nothing. I'd correct or withdraw the review.

**Real issues (all small, written to `findings.json` in the repo root, 8 items):**

- **`move_topic`, medium.** `new_parent_id` is never checked against `new_path`. A wrong or in-subtree parent leaves `parent_id` and `path` disagreeing, or creates a cycle. Nothing in the schema enforces that they agree. Derive the parent from `new_path`, or validate it.
- **`move_topic`, low.** A move on a nonexistent `old_path` silently does nothing.
- **LIKE index use is undocumented and untested, low.** It depends on the NOCASE collation, `case_sensitive_like` being off, and no leading wildcard. Add a comment and an `EXPLAIN QUERY PLAN` test, or use an explicit range comparison.
- **`ORDER BY updated_at DESC LIMIT 100`, low.** It sorts every article in the subtree in a temp b-tree. That is fine now, but it is the one cost that grows with a big account's top-level page. Measure the largest real tree before touching the schema.
- **`topic.path` CHECK, low.** `GLOB '/*/'` allows `//` and empty segments, which `tree.py` would reject.
- **`PATH` regex in `tree.py`, low.** `$` allows a trailing newline. Use `fullmatch`.
- **Foreign keys, low.** They are not enforced unless the connection sets `PRAGMA foreign_keys=ON`. `topic_parent` is unused by any query.

The sample data is clean: no cycles, no `parent_id`/`path` mismatches, no orphaned articles, no empty segments.
