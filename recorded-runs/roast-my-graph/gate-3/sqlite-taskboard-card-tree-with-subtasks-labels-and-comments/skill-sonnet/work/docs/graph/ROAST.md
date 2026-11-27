# Roast: taskboard storage (db/schema.sql, app/cards.py, app/db.py)

Verdict: Yes, every query in app/cards.py hits an index, and that is exactly why the one thing that does not is invisible. One serious problem: the foreign key that cascades deletes through subtasks (`card.parent_id`) has no index that leads with it, so every card deleted costs a full scan of `card`. Everything else holds up.

Judged against:
- Engine: SQLite via Python `sqlite3`, one database file per workspace (README.md). Version of the SQLite library: not stated in the repo; plans below were run on SQLite 3.53.1.
- Size: largest workspace 2.1 million cards (README.md). `board.db` sample: 200 boards, 200,000 cards (59,793 top-level, 97,670 at depth 3 or deeper), 1,000 labels, 80,154 card_label rows, 199,375 comments, 1,000 cards per board.
- Operations: deleting a card from the card menu in the browser, and "Clear done column" which deletes every card in a column (README.md, `delete_card`, `clear_done_column`). Both are interactive.
- Invariants: deleting a card deletes its whole subtree, labels and comments through cascading foreign keys (README.md, db/schema.sql). `PRAGMA foreign_keys = ON` is set in `connect()` in app/db.py, so the cascade does run.

## Findings

### critical: `parent_id`
Every query hit an index, and the one nobody wrote still reads the whole table. The planner would like a word, and the word is SCAN.
Problem: When `delete_card` or `clear_done_column` deletes a card, SQLite must find its children with `WHERE parent_id = ?` and delete them, then do the same for each of their children. The only index containing `parent_id` is `card_board_parent (board_id, parent_id)`, which leads with `board_id`, so the cascade lookup cannot search it. Run on board.db with foreign keys on, `DELETE FROM card WHERE id = ?` plans as `SEARCH card USING INTEGER PRIMARY KEY` for the row itself, then `SCAN card USING COVERING INDEX card_board_parent` for the child lookup (and `DELETE FROM card WHERE parent_id=5` plans as a plain `SCAN card`). That is one pass over the whole `card` index per deleted card, not per statement: a subtree of k cards costs k passes. At the README's 2.1 million cards, deleting one card with a 50-card subtree is about 50 scans of 2.1 million entries, and "Clear done column" multiplies that by every top-level card in the column. The delete runs inside one transaction holding the write lock for all of it. The statements in app/cards.py never show this, because the cost is in the foreign key, not in any query text, so EXPLAIN QUERY PLAN on them cannot find it.
Fix: Add an index that leads with the foreign key column: `CREATE INDEX card_parent ON card (parent_id);` in db/schema.sql, and run the same statement on existing databases (it is a plain index on an existing column, no data migration). Re-check with `EXPLAIN QUERY PLAN DELETE FROM card WHERE id = ?` that the child lookup now reads `SEARCH card USING COVERING INDEX card_parent (parent_id=?)`. Keep `card_board_parent`: `top_level` and `subtasks` use it.

## Holds up
- `card_board_parent`: serves `top_level` (board_id, `parent_id IS NULL`, ordered by id because rowid trails the index) and `subtasks` (board_id, parent_id). Both plan as a SEARCH. It just cannot serve the cascade, which is the finding above.
- `card_board_column`: `column` filters `parent_id IS NULL` after the index search, so about 70 percent of the rows it reads are subtasks that are thrown away (sample: 5 columns, about 200 cards per board and column). With 1,000 cards per board in the sample that is trivial; it would only matter if the README stated boards in the hundreds of thousands, which it does not.
- `card_label`: the composite primary key (card_id, label_id) serves `labels_of` and the cascade from `card`; `card_label_by_label` serves the cascade from `label`. `WITHOUT ROWID` fits a pure link table. Nothing else points at it, but it joins two entities and carries no extra data, so it is already the minimal shape.
- `comment_card`: leads with `card_id`, serves both `comments_of` (with the created_at order) and the cascade, which plans as a covering SEARCH.
- `label_board`: serves the cascade from `board`.
- `connect`: turns `PRAGMA foreign_keys` on, so the cascade the README promises holds for every writer that uses this function. No other path to the database is in the repo.
- `parent_id` nesting: depth is unbounded (97,670 sample cards sit at depth 3 or deeper), but the cascade is a tree walk over a foreign key to the same table and the shipped data has no cycle trouble to report; no recursive query in the repo.

## Not checked
- Actual timing at 2.1 million cards: the sample has 200,000, so the plan shape is verified and the cost is stated from row counts, not measured. I ran EXPLAIN QUERY PLAN only, read-only (`mode=ro`); nothing was written, so the fix was not applied to a copy.
- SQLite version in production: not stated; plans were taken on 3.53.1.
- Other writers to the database file outside this repo: none visible.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
