The indexes you checked do their job for the SELECTs. The real problem is in the delete path, which EXPLAIN QUERY PLAN on your queries never shows.

**Critical: deletes scan the whole card table.** `card.parent_id` has `ON DELETE CASCADE`, but no index starts with `parent_id`. `card_board_parent` is `(board_id, parent_id)`, so the cascade's `WHERE parent_id = ?` can't use it. Every deleted card, leaf or not, triggers a full SCAN of `card`. I checked this on an in-memory copy of board.db with foreign keys on (the file itself was not modified):

- One leaf card: 38 ms
- One top-level card with a 155-card subtree: 2.7 s
- One column of one board (`clear_done_column`): 6.6 s
- All 1000 cards of one board: 32 s

`CREATE INDEX card_parent ON card (parent_id);` brings the leaf delete to 0.1 ms, one column clear to 2 ms and one board delete to 10 ms. I did not re-time the 155-card subtree case with the index. Cost grows with rows deleted times table size, so the 2.1M-card workspace will be much worse than the sample. Also batch large deletes so no single write transaction holds the lock for seconds.

**High: `clear_done_column` does not only clear done cards.** It deletes every top-level card in the column. In the sample, column 0 has 11,695 top-level cards, and 8,168 of them are not done. The name and the UI label say "done", while the README says every card in the column. Confirm which is intended, then either filter on `done = 1` or rename the function and the label and add a count-based confirmation.

**High: `top_level` is unbounded.** It calls `fetchall()` with no LIMIT. About 299 top-level cards per board in the sample becomes hundreds of thousands of rows on the largest workspace. Use keyset pagination (`id > ? ORDER BY id LIMIT ?`).

**Medium: `column` overscans.** `card_board_column` lacks `parent_id`, so the query reads subtasks too: 187 rows read for 51 returned on board 1, column 0; 39,783 read for 11,695 returned across the sample. A partial index `ON card (board_id, column_no) WHERE parent_id IS NULL` matches the query. The query also needs a LIMIT.

**Medium: `connect` has no WAL and no explicit timeout.** A long delete blocks writers, and anything waiting over Python's default 5 s gets "database is locked". Set `journal_mode = WAL`, set an explicit timeout, and keep write transactions short.

**Low: `comments_of`.** `created_at` holds date-only values in the sample, so same-day comments have undefined order. Add a time component or `id` as a tie-breaker.

One note on the sample: board.db is 200 boards of 1000 cards each, not one large board. Per-board timings here understate what the 2.1M-card workspace will see.

All six findings are in `findings.json` in the repo root (`/run/work/findings.json`).
