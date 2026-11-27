// What: add :Dormant to passengers whose last tour ended before 2024-01-01 (docs/mailing.md); enquirers (no lastTravelled) are left alone.
// Count before/after: MATCH (p:Passenger) WHERE p.lastTravelled < date('2024-01-01') AND NOT p:Dormant RETURN count(p)
MATCH (p:Passenger) WHERE p.lastTravelled < datetime('2024-01-01T00:00:00Z')
CALL (p) { SET p:Dormant } IN TRANSACTIONS OF 10000 ROWS;
