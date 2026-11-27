// what: delete the trips that ended before 2024-01-01 with their TOOK, USED, STARTED_IN and BILLED_ON relationships
// why: past retention (docs/retention.md); invoices, members, cars and zones stay
// count: MATCH (t:Trip) WHERE t.endedAt < datetime('2024-01-01T00:00:00Z') RETURN count(t);
MATCH (t:Trip)-[r]-()
WHERE t.endedAt < datetime('2024-01-01T00:00:00Z')
CALL (r) { DELETE r } IN TRANSACTIONS OF 10000 ROWS;
MATCH (t:Trip)
WHERE t.endedAt < datetime('2024-01-01T00:00:00Z') AND NOT (t)--()
CALL (t) { DELETE t } IN TRANSACTIONS OF 10000 ROWS;
