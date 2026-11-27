Added sql/pairs_with.sql. It reads each pairing in both directions (pairs are stored once, product_a < product_b)
and returns the products one or two pairings away, without the product itself: the two-step limit merch set, as
recorded in docs/graph/DECISION.md (no-graph: two joins on Postgres, no graph database). Checked on a SQLite
database built from db/schema.sql.
