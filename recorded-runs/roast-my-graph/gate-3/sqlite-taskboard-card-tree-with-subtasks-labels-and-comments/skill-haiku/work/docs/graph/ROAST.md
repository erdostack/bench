# Roast: taskboard storage (app/ and db/)

Verdict: One critical. The foreign key `card.parent_id` has no index that leads with it, so every cascading delete scans the whole `card` table once per deleted row. Your EXPLAIN sweep was right about the SELECTs and blind to the DELETEs, because the cascade never shows up in a query you run.

Judged against:
- Engine: SQLite through Python `sqlite3` (`app/db.py`). Version not stated in the repo; measured on SQLite 3.53.1.
- Largest workspace: 2.1 million cards (`README.md`). Sample `board.db`: 200,000 cards, 200 boards, 80,154 `card_label` rows, 199,375 comments (measured).
- Interactive: browsing top-level cards, a board column, subtasks, labels and comments (`app/cards.py`); deleting a card from the card menu (`delete_card`); "Clear done column" (`clear_done_column`). The README states both deletes cascade to subtasks, labels and comments.
- Writers: only `app/db.py` and `app/cards.py`; every connection sets `PRAGMA foreign_keys = ON`.
- Stated invariant: deleting a card removes its whole subtree, labels and comments (`README.md`).

## Findings

### critical: `card.parent_id`
Every card that is deleted makes SQLite look up its children by `parent_id`. The only index that touches `parent_id` is `card_board_parent (board_id, parent_id)`, which leads with `board_id`, so the cascade cannot search it and reads all of it. Each deleted row costs one pass over the whole table. It is the foreign key that has no index on the child column, and the cascade is what finds it.
Problem: When "Clear done column" (`clear_done_column`) or `delete_card` runs on a card with subtasks in a workspace the README states has 2.1 million cards, SQLite scans `card` once for every deleted row to find its children. `EXPLAIN QUERY PLAN SELECT id FROM card WHERE parent_id = ?` on the sample reports `SCAN card USING COVERING INDEX card_board_parent`. Measured on an in-memory copy of the 200,000-card sample: clearing one column of board 1 (343 rows, cascades included) took 5.13 s without a `parent_id` index and 0.010 s with one; deleting a root with a 378-row subtree took 6.41 s and 0.006 s. At 2.1 million cards each scan reads about ten times as many index entries, so the same deletes are expected to take minutes at a few thousand rows (estimate, not measured). The whole statement runs inside one write transaction, so the delay also holds the write lock.
Fix: add the index to `db/schema.sql`:

```sql
CREATE INDEX card_parent ON card (parent_id);
```

Keep `card_board_parent`; the top-level and subtask reads still use it. Stored data does not change, so the migration is to run the statement once on each existing workspace file (build time on a 2.1 million-card file not measured). On a copy of the sample the cascade lookup plan became `SEARCH card USING COVERING INDEX card_parent (parent_id=?)`.

### low: `card_board_column`
The column read and "Clear done column" search `card_board_column (board_id, column_no)`, which also holds every subtask in that column. The `parent_id IS NULL` filter then throws the subtasks away after they are read. Sample, board 1 column 2: 205 indexed cards, 60 of them top-level, so about 3.4 times the index entries are read for each column view.
Problem: When `column()` runs on a board that has many subtasks in one column, the index search reads all of the column's cards and the filter discards the subtask rows. The cost tracks the subtask count, and the README states no board size, so this stays low until boards get large.
Fix: replace the index so the filter column is part of the key:

```sql
DROP INDEX card_board_column;
CREATE INDEX card_board_column ON card (board_id, column_no, parent_id);
```

On the in-memory copy the plan became `SEARCH card USING INDEX card_board_column (board_id=? AND column_no=? AND parent_id=?)`.

## Holds up
- `card_board_parent (board_id, parent_id)`: `top_level` and `subtasks` plan as searches on it, and `subtasks` sorts by `id` with no separate sort step. It is the right index for those reads; it cannot serve the cascade, which is the critical finding above.
- `comment_card (card_id, created_at)`: `comments_of` plans as a search on `card_id` and the `ORDER BY created_at` needs no sort step. The cascade from `card` into `comment` also uses it.
- `card_label` primary key `(card_id, label_id)` and `WITHOUT ROWID`: `labels_of` searches it by `card_id`, and the cascade from `card` into `card_label` uses the same key.
- `card_label_by_label (label_id, card_id)` and `label_board (board_id)`: serve the cascades from `label` and `board`. No code in `app/` deletes labels or boards, so these cost only on writes.
- `delete_card` and `labels_of` join: the card's own delete and the label join plan as primary-key searches.
- Sample data: no child with a different `board_id` from its parent, no orphan `parent_id`, no self-parenting, no `card_label` row whose card and label sit on different boards. Maximum nesting in the sample is 15 levels.

## Not checked
- No `DELETE` was run against `board.db`. It is opened read-only, there is no `docs/graph/CONTEXT.md` to say otherwise, and `engines.md` says not to run writes in that case. The delete timings come from in-memory copies of the sample made with the SQLite backup API; the file was not changed.
- The 2.1 million-card cost is an extrapolation from the 200,000-card sample. Only the sample was timed.
- I inferred that the cascade uses the same lookup as the `SELECT ... WHERE parent_id = ?` I explained. The timings match a scan per deleted row, but I did not read SQLite's foreign-key implementation.
- Nesting depth: the files set no cap on how deep subtasks can go, and the cascade runs as nested triggers in SQLite. I did not test a chain deep enough to hit the engine's trigger-depth limit, and I did not confirm that limit against the SQLite docs.
- The repo has no tests, and `app/` has no insert path, so the data was checked only as stored in `board.db`.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
