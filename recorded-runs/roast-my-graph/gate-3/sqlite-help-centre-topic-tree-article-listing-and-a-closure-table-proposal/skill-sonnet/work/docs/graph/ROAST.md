# Roast: helpdesk-kb (schema.sql, queries/, kb/)

Verdict: No, a closure table is not warranted. The review's premise is wrong: in SQLite 3.53.1, `LIKE '<prefix>%'` on `topic.path` is an index search, not a scan, so the topic page does not read 400,000 rows. Nothing serious: three `low` notes, none of which needs a redesign.

Judged against:
- Engine: SQLite (README.md); the sample ran on SQLite 3.53.1. Production version: not stated.
- Size: about 400,000 topics (one tree per customer account) and 2 million articles in production; `kb.db` is a 40,000-topic, 160,000-article, 200-account sample (README.md, kb.db).
- Reads: a topic page lists every article in the topic and below, via `articles_under()` and `queries/subtree_articles.sql` with the pattern `<topic path>%` (README.md, kb/tree.py).
- Writes: topic moves are rare, a few per month, through `queries/move_topic.sql` (README.md).
- Invariants: paths are lower case, `[a-z0-9-/]`, start and end with `/`, enforced by CHECKs on `topic.path` (README.md, schema.sql). Accounts per production size and the largest tree: not stated.

## Findings

### low: `subtree_articles.sql`
The page is cheap to find and then pays to sort: the planner finds the subtree in one index range, then sorts everything it finds.
Problem: Question to confirm: the statement sorts every article in the subtree (`USE TEMP B-TREE FOR ORDER BY`) before `LIMIT 100`, so a topic page costs rows proportional to the subtree's article count. The README gives totals but not the largest account's size. The topic lookup itself is an index search on `sqlite_autoindex_topic_1`.
Fix: Count the largest account's articles (`SELECT count(*) FROM topic t JOIN article a ON a.topic_id = t.id WHERE t.path LIKE '/<account>/%'`). At about 5 articles per topic, a 2,000-topic account is about 10,000 rows sorted per view, which is fine. Change nothing unless the biggest tree is far larger. A closure table would not remove the sort.

### low: `move_topic`
Problem: `new_path` and `new_parent_id` are independent arguments and nothing checks they agree. On an in-memory copy of `kb.db`, moving `/acct-2/x/` to `/acct-3/y/` with the parent id of `/acct-2/` was accepted, leaving `parent_id` and `path` disagreeing. The sample has 0 mismatches today and no caller in the files passes a wrong pair, so this is hardening.
Fix: derive the parent inside the function: `parent_path = new_path[:new_path.rstrip('/').rfind('/') + 1]`, look up `SELECT id FROM topic WHERE path = ?`, raise `ValueError` if it is missing or differs from `new_parent_id`, and use the looked-up id in the `UPDATE`.

### low: `topic_parent`
Problem: nothing in `queries/` or `kb/tree.py` reads or filters on `parent_id`; `move_topic` only writes it, finding the row by path. The index is maintained on every insert and parent change and serves no stated read.
Fix: keep the `parent_id` column (foreign key, and the right base for a recursive walk). If no by-parent lookup is planned, `DROP INDEX topic_parent;` and recreate it when one exists.

## Holds up
- `path` (stored full path with CHECKs): the one stored copy of the hierarchy, and it is sound. The stated read (all articles under a topic) is a prefix range; the `UNIQUE COLLATE NOCASE` constraint creates `sqlite_autoindex_topic_1`, which is exactly the index SQLite's LIKE prefix optimisation needs because LIKE is case-insensitive by default. `EXPLAIN QUERY PLAN` shows `SEARCH t USING COVERING INDEX sqlite_autoindex_topic_1 (path>? AND path<?)`. Moves are rare and `move_topic` rewrites paths and `parent_id` in one transaction. The CHECKs and the `PATH` regex keep `%`, `_` and any other LIKE wildcard out of both path and pattern, and the trailing `/` stops `/acct-1/` matching `/acct-10/`. Checked on the sample: the subtree query returns the same 803 articles for `/acct-1/` as a recursive walk over `parent_id`. What would change this: a read that is not a prefix of the path (for example "all topics with this title anywhere"), or moves becoming frequent and large.
- `queries/move_topic.sql`: the `WHERE path LIKE :old_pattern` is also an index search (`SEARCH topic USING INDEX sqlite_autoindex_topic_1 (path>? AND path<?)`), and the rewrite touches only the moved subtree. The guard `new_path.startswith(old_path)` in `move_topic` stops a topic being moved under itself.
- `article_topic`: leads with `topic_id`, the join column, and the plan shows `SEARCH a USING INDEX article_topic (topic_id=?)`.
- Closure table (`topic_closure`) proposal: not adopted. It would store one row per ancestor-descendant pair (about 400,000 times the average depth) and maintain it with triggers, and every move would delete and reinsert closure rows for each descendant crossing the old and new ancestors, where today it is one indexed `UPDATE`. It would speed up nothing the index range does not already do.

## Not checked
- Speed at production size: the sample shows plan shape only. Nothing was timed against 400,000 topics.
- The production SQLite version and whether the LIKE prefix optimisation behaves the same there. It needs the default case-insensitive LIKE (no `PRAGMA case_sensitive_like`) and a statement prepared with the bound value, which Python's `sqlite3` does.
- `PRAGMA foreign_keys`: the repo never opens a connection, so whether production enables foreign keys is not stated.
- Writes were not run against `kb.db`; the move test used an in-memory copy.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
