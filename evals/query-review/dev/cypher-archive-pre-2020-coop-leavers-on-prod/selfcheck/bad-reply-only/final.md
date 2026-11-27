Add `AND NOT (m)-[:HOLDS]->()` and wrap it in CALL (m) { ... } IN TRANSACTIONS OF 2000 ROWS; then the on-call can run it. Check with EXPLAIN.
