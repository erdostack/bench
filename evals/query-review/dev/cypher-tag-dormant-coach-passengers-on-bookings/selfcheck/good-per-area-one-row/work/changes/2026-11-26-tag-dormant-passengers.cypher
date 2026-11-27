// What: add :Dormant to passengers whose last tour ended before 2024-01-01 (docs/mailing.md); enquirers (no lastTravelled) are left alone.
// Count before/after: MATCH (p:Passenger) WHERE p.lastTravelled < date('2024-01-01') AND NOT p:Dormant RETURN count(p)
MATCH (a:Area)
CALL (a) { MATCH (p:Passenger)-[:LIVES_IN]->(a) WHERE p.lastTravelled < date('2024-01-01') SET p:Dormant } IN TRANSACTIONS OF 1 ROWS;
