// 032: delete every Pass with validUntil before 2026-01-01 (renewed or lapsed; clutter on harbour), together with its
// HELD_BY, COVERS and BOARDED relationships. Customers, Routes and Sailings stay. Expect about 38,000 passes
// (docs/model.md; confirm with the count below) and, with their relationships, roughly 2 to 3 million deletes in all.
// A pass has at most 405 relationships (docs/model.md), so 20 passes per transaction is at most 20 x 406 = 8,120
// nodes and relationships, under the 10,000 limit in docs/changes.md. A re-run carries on with what is left.
// Count before (about 38,000) and after (0):
//   MATCH (p:Pass) WHERE p.validUntil < date('2026-01-01') RETURN count(p);
// Check afterwards that nothing else went: MATCH (c:Customer) RETURN count(c); (about 14,000, unchanged) and
//   MATCH (s:Sailing) RETURN count(s); (about 52,000, unchanged).
// Reviewer: please run EXPLAIN on the statement below first; nothing here was run (no copy of harbour exists).
MATCH (p:Pass)
WHERE p.validUntil < date('2026-01-01')
CALL (p) {
  DETACH DELETE p
} IN TRANSACTIONS OF 20 ROWS;
