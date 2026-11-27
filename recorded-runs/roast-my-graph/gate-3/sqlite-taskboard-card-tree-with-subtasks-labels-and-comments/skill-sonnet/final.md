Verdict: you are right that every query hits an index, and that is why the real problem is hiding. One critical finding, everything else holds up.

Critical, `parent_id`: the ON DELETE CASCADE on `card.parent_id` has no index that leads with `parent_id` (the only one is `card_board_parent (board_id, parent_id)`). Each deleted card triggers a lookup of its children that scans the whole `card` table. I confirmed on board.db that `DELETE FROM card WHERE id = ?` plans a `SCAN card USING COVERING INDEX card_board_parent` for the child lookup. A subtree of k cards costs k full scans, and at the README's 2.1 million cards "Clear done column" multiplies that by every top-level card in the column, all inside one write transaction. EXPLAIN QUERY PLAN on the statements in app/cards.py cannot show it because the cost lives in the foreign key.
Fix: `CREATE INDEX card_parent ON card (parent_id);` (no data migration), then re-check the plan.

Everything else (the other indexes, `card_label`, `comment_card`, `connect` enabling foreign keys) holds up; reasons are in the roast. I only ran read-only EXPLAIN QUERY PLAN on the 200k-row sample, so the cost at 2.1 million cards is derived from plan shape and row counts, not timed.

Files: docs/graph/ROAST.md and findings.json (repo root, same single finding) in /run/work.
