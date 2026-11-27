// 032: delete passes that expired before 2026-01-01 (validUntil < date('2026-01-01')), with their HELD_BY,
// COVERS and BOARDED relationships. Customers, routes and sailings stay. Renewals are done (requested by: TBD).
// Expect about 38,000 Pass nodes. Count before (should be about 38,000) and after (should be 0):
//   MATCH (p:Pass) WHERE p.validUntil < date('2026-01-01') RETURN count(p);
// Batch size: a pass has at most 405 relationships (1 HELD_BY + 4 COVERS + 400 BOARDED), so at most 406
// nodes and relationships deleted per pass. 24 x 406 = 9,744, under the 10,000 per-transaction cap.
// Safe to re-run: it only matches passes still present.
// Reviewed by: PENDING. Not yet run on harbour.
MATCH (p:Pass)
WHERE p.validUntil < date('2026-01-01')
CALL (p) {
  DETACH DELETE p
} IN TRANSACTIONS OF 24 ROWS;
