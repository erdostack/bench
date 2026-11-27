// OPS-412: November 2026 quote clean-up. Deletes quotes never converted to a hire (status draft, sent or declined)
// with validUntil before 2026-11-01, with their FOR and LINE relationships. Converted quotes are never deleted.
// Batches of 200 quotes: at most 200 x 42 nodes and relationships per transaction, under the 10,000 limit.
// Count before the run (expected count, recorded by the reviewer: ____):
//   MATCH (q:Quote) WHERE q.status IN ['draft', 'sent', 'declined'] AND q.validUntil < date('2026-11-01') RETURN count(q);
// Count after the run (0 expected):
//   MATCH (q:Quote) WHERE q.status IN ['draft', 'sent', 'declined'] AND q.validUntil < date('2026-11-01') RETURN count(q);
// Reviewed by: (blank until review)
MATCH (q:Quote)
WHERE q.status IN ['draft', 'sent', 'declined'] AND q.validUntil < date('2026-11-01')
CALL (q) {
  DETACH DELETE q
} IN TRANSACTIONS OF 200 ROWS;
