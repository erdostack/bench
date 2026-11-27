Second opinion: keep the paths. None of the three claims holds for this code.

- Wrong results: every id is closed by a slash on both sides and the CHECKs refuse anything else, so the
  pattern for park 12 cannot pick up park 120. I made 40 random moves on a copy of parks.db and compared
  subtree() with an independent model of the tree for 300 rows; every one matched.
- Index: the pattern is bound as one parameter, so SQLite turns the GLOB into a range search on the unique
  index on path. EXPLAIN QUERY PLAN shows that for subtree, children and due_under.
- Moves: one UPDATE rewrites the moved subtree and nothing else, in one transaction, a few times a year.

At 90,000 rows this stays fast. Two low notes in findings.json and docs/graph/ROAST.md.
