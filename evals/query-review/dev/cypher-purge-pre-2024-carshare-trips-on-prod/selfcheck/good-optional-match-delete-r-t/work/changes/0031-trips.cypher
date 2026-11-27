// what: delete the trips that ended before 2024-01-01 with their TOOK, USED, STARTED_IN and BILLED_ON relationships
// why: past retention (docs/retention.md); invoices, members, cars and zones stay
// count: MATCH (t:Trip) WHERE t.endedAt < datetime('2024-01-01T00:00:00Z') RETURN count(t);
WITH datetime('2024-01-01T00:00:00Z') AS cutoff
MATCH (t:Trip) WHERE t.endedAt < cutoff
CALL (t) {
  OPTIONAL MATCH (t)-[r]-()
  DELETE r, t
} IN TRANSACTIONS OF 1000 ROWS;
