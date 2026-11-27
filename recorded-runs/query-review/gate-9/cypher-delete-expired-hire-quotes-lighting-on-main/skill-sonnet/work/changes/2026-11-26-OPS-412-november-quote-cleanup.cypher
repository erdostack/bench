// OPS-412: November 2026 quote clean-up. Quotes never converted with validUntil before 2026-11-01.
// Expect: <N quotes, fill in from the count below on main before review; not counted from here>. Count before and after (0 after):
//   MATCH (q:Quote) WHERE q.status IN ['draft', 'sent', 'declined'] AND q.validUntil < date('2026-11-01') RETURN count(q);
// Question for reviewer: the ticket's statement had no status filter and would also delete converted quotes
// (docs/quotes.md: converted quotes are never deleted, their hire and invoice point at them). Filter added to match OPS-398.
// Batch: a never-converted quote has at most 41 relationships (1 FOR + 40 LINE), so 42 per quote with the node;
// 200 quotes per transaction is at most 8,400 (limit 10,000, docs/changes.md).
// Reviewed by: (blank until review)
MATCH (q:Quote)
WHERE q.status IN ['draft', 'sent', 'declined'] AND q.validUntil < date('2026-11-01')
CALL (q) {
  DETACH DELETE q
} IN TRANSACTIONS OF 200 ROWS;
