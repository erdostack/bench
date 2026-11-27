// OPS-412: November 2026 quote clean-up. Quotes never converted with validUntil before 2026-11-01.
// Expect: to be filled in from the count below before review. Count before and after (0 after):
//   MATCH (q:Quote) WHERE q.status IN ['draft', 'sent', 'declined'] AND q.validUntil < date('2026-11-01') RETURN count(q);
// Batches of 200 quotes: at most 42 nodes and relationships each (the quote, one FOR, up to 40 LINE), 8,400 per transaction.
// Reviewed by: (pending, ops lead)
MATCH (q:Quote)
WHERE q.status IN ['draft', 'sent', 'declined'] AND q.validUntil < date('2026-11-01')
CALL (q) {
  DETACH DELETE q
} IN TRANSACTIONS OF 200 ROWS;
