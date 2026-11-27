// what: delete every Trip that ended before 2024-01-01T00:00:00Z, with its TOOK, USED, STARTED_IN and BILLED_ON relationships; Invoice, Member, Car and Zone nodes are kept
// why: docs/retention.md, a trip is kept until the end of the second full calendar year after it ended, so trips that ended before 2024 are past that now. Also the trip history queries are slow on the full table.
// count before: MATCH (t:Trip) WHERE t.endedAt < datetime('2024-01-01T00:00:00Z') RETURN count(t);
// count after (should be 0): MATCH (t:Trip) WHERE t.endedAt < datetime('2024-01-01T00:00:00Z') RETURN count(t);
// batching: at most 4 relationships and 1 node per trip, so 1000 trips is at most 5,000 changes, under the 10,000 per transaction limit in docs/environment.md
// not run: awaiting review and a run by the fleet on-call with bin/tq prod --file changes/0031-delete-trips-ended-before-2024.cypher
MATCH (t:Trip)
WHERE t.endedAt < datetime('2024-01-01T00:00:00Z')
CALL (t) {
  DETACH DELETE t
} IN TRANSACTIONS OF 1000 ROWS;
