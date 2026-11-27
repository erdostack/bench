// what: delete the trips that ended before 2024-01-01 with their TOOK, USED, STARTED_IN and BILLED_ON relationships
// why: past retention (docs/retention.md); invoices, members, cars and zones stay
// count: MATCH (t:Trip) WHERE t.endedAt < datetime('2024-01-01T00:00:00Z') RETURN count(t);
MATCH (:Member)-[r:TOOK]->(t:Trip) WHERE t.endedAt < datetime('2024-01-01T00:00:00Z')
CALL (r) { DELETE r } IN TRANSACTIONS OF 5000 ROWS;
MATCH (t:Trip)-[r:USED|STARTED_IN|BILLED_ON]->() WHERE t.endedAt < datetime('2024-01-01T00:00:00Z')
CALL (r) { DELETE r } IN TRANSACTIONS OF 5000 ROWS;
