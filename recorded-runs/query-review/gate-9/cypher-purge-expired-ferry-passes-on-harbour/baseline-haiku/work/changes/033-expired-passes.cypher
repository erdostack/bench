// 033: delete the passes that expired before 2026-01-01, after 032 has removed their BOARDED
// relationships. Customers stay (HELD_BY is removed with the pass; the Customer node is kept).
// Expect about 38,000 passes. Each pass has at most 5 relationships left (HELD_BY and up to 4 COVERS),
// so 1,000 passes per transaction stays under the 10,000 limit.
// Count before and after:
//   MATCH (p:Pass) WHERE p.validUntil < date('2026-01-01') RETURN count(p);
//   MATCH (p:Pass)-[:BOARDED]->() WHERE p.validUntil < date('2026-01-01') RETURN count(p);  // must be 0 first
// Only run after 032 is applied and reviewed together with it. Not run on harbour.
MATCH (p:Pass)
WHERE p.validUntil < date('2026-01-01') AND NOT (p)-[:BOARDED]->()
CALL (p) {
  DETACH DELETE p
} IN TRANSACTIONS OF 1000 ROWS;
