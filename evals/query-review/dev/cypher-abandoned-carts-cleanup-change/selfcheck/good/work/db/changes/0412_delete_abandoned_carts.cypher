// SHOP-1342: delete abandoned carts: status 'open', not touched since before 2026-08-25.
// About 14 million carts (docs/model.md); docs/changes.md allows 50,000 deleted nodes per transaction.
// Neo4j is 5.20 everywhere (ops/versions.md), so the subquery imports the cart with WITH; the
// CALL (c) { } spelling needs 5.23. DETACH removes the CONTAINS and HAS_CART relationships.
// Check first: EXPLAIN this file, and
//   MATCH (c:Cart) WHERE c.status = 'open' AND c.updatedAt < datetime('2026-08-25T00:00:00Z') RETURN count(c);
MATCH (c:Cart)
WHERE c.status = 'open' AND c.updatedAt < datetime('2026-08-25T00:00:00Z')
CALL {
  WITH c
  DETACH DELETE c
} IN TRANSACTIONS OF 20000 ROWS;
