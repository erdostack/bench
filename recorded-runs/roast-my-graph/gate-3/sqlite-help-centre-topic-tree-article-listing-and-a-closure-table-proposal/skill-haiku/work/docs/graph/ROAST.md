# Roast: helpdesk-kb (topic tree, SQLite)

Verdict: Nothing serious. The closure table is not warranted: the subtree `LIKE` already searches the `path` index on SQLite 3.53.1, so the "full scan of topic" in `docs/review.md` does not happen in this schema. The real cost is the sort in the topic-page query, and that is a medium, not a reason to add a table that every insert and move would have to maintain.

Judged against:
- Engine: SQLite, from `kb.db` and `kb/tree.py` (no version stated in the repo; plans checked on SQLite 3.53.1).
- Production size: about 400,000 topics and 2 million articles (`README.md`). Sample: 40,000 topics and 160,000 articles (`kb.db`, counted).
- Interactive path: a topic page runs `queries/subtree_articles.sql` (`README.md`).
- Rare writes: editors move topics a few times a month (`README.md`, `queries/move_topic.sql`).
- Stated invariant: paths are lower case, made of letters, digits, `-` and `/`, and start and end with `/` (`README.md`, CHECK in `schema.sql`).
- Writers: `kb/tree.py` (`move_topic`). No insert code is in the repo.

## Findings

### medium: `queries/subtree_articles.sql`
The query gathers every article under the prefix, sorts them all by `updated_at`, and only then keeps 100. The index work is fine. The sort is not.
Problem: When a topic page runs on a large subtree (a root or an account topic), SQLite reads every article under that prefix and builds a temp B-tree for `ORDER BY a.updated_at DESC` before `LIMIT 100`. Measured on the sample: 738 articles under `/acct-191/` took about 28 ms, 88,988 articles under `/acct-1` took about 84 ms, and all 160,000 articles took about 32 ms. Cost grows with the subtree's article count, so at 2 million articles a root-level page is expected to be about 12 times slower. That scaling is an estimate, not measured.
Fix: Measure at production size first. If it is too slow, remove the cause: the newest-100 across a prefix cannot come from one index walk, so keep a per-subtree recent-articles table written by the article write path in the same transaction, and read the top 100 from it. Confirm the plan with `EXPLAIN QUERY PLAN` on a 2-million-row copy.

### medium: `topic.parent_id`
The foreign key is declared, but nothing turns enforcement on, and `move_topic` accepts any parent id.
Problem: `REFERENCES topic(id)` is not enforced because `PRAGMA foreign_keys` is off on a new connection and `kb/tree.py` never sets it. `move_topic(con, '/acct-191/integrations-38028/', '/acct-192/integrations-38028/', 999999)` ran without error in an in-memory copy and left one row whose `parent_id` points at nothing. No query in the repo reads `parent_id`, so no page is wrong today; the fact is duplicated with no check tying it to `path`.
Fix: Derive the parent in the statement from the new path, not from the caller: `UPDATE topic SET parent_id = (SELECT id FROM topic WHERE path = :new_parent_path) WHERE path = :old_path;`, and raise if no row matched. Also open connections with `PRAGMA foreign_keys = ON`. Or drop `parent_id` and read the parent from `path`, if nothing else needs it.

### low: `topic_parent`
Problem: The index on `topic(parent_id)` serves no query in the repo. Every insert and move pays to maintain it.
Fix: Drop it (`DROP INDEX topic_parent;`) unless a reader of `parent_id` is added. Keep it only together with the `parent_id` fix above.

### low: `move_topic` (kb/tree.py)
Problem: When `old_path` does not exist, both statements change zero rows and the function returns normally. Measured in an in-memory copy: a move from `/acct-191/no-such-topic/` made 0 changes and raised nothing, so the caller believes the move happened.
Fix: Check `cursor.rowcount` after the first `UPDATE` and raise `ValueError` when it is 0, inside the same `with con:` block.

### low: `PATH` (kb/tree.py)
Problem: The pattern `^/(?:[a-z0-9-]+/)*$` uses `$`, which also matches before a trailing newline. `PATH.match("/acct-191/\n")` returns a match, so the newline reaches the `LIKE` pattern and the query returns nothing with no error.
Fix: Use `PATH.fullmatch(...)` (or `\Z`) in both checks.

### low: `topic.path` (CHECK in schema.sql)
Problem: The CHECK accepts `//`. Measured in an in-memory copy: an insert with path `/acct-191//` succeeded. `kb/tree.py` rejects the same string, so the schema is looser than the README and the code.
Fix: Add `AND path NOT GLOB '*//*'` to the CHECK, in a migration that rebuilds `topic` (SQLite cannot alter a CHECK in place). The sample has no such rows (counted), so the migration is a formality.

## Holds up
- `topic.path` (UNIQUE, `COLLATE NOCASE`) with `WHERE path LIKE :pattern`: planned as `SEARCH t USING COVERING INDEX sqlite_autoindex_topic_1 (path>? AND path<?)` with the bound parameter and with a literal, on SQLite 3.53.1. The subtree lookup is a range search. It would stop being one if the column lost `NOCASE` (the `LIKE` optimisation depends on it), so keep that collation.
- `topic.path` as a stored full path: a copy of the parent chain, but it makes a subtree one prefix range. The write path (`move_topic`) updates `parent_id` and every path under the moved topic in one transaction, and a collision rolls back both (checked: the `UNIQUE` failure left the row unchanged).
- `move_topic.sql` (`WHERE path LIKE :old_pattern`): planned as an index search, and moves are rare. A scan here would not matter.
- `article_topic (topic_id, updated_at)`: serves the join from `topic` to `article` by `topic_id`.
- A closure table: it would duplicate what the prefix range already gives, and each insert would need trigger work, and each move would rewrite one row per descendant pair. The benefit is not there at this read cost.

## Not checked
- Production size (2 million articles, 400,000 topics) was not run. The sample is 160,000 articles, so the cost at scale is an estimate.
- Production SQLite version is not stated; plans were checked on 3.53.1.
- Writers other than `kb/tree.py` (topic inserts, article loads) are not in the repo, so whether they enable foreign keys is unknown.
- Same-statement `UNIQUE` collisions inside a single subtree move were not searched exhaustively; the tested cases behaved correctly.
- `kb.db` was opened read-only (`mode=ro`), and the move tests ran on an in-memory copy. `kb.db` was not changed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
