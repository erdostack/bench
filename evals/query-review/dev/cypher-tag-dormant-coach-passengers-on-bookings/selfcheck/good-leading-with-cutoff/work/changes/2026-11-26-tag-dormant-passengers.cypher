// What: add :Dormant to passengers whose last tour ended before 2024-01-01 (docs/mailing.md); enquirers (no lastTravelled) are left alone.
// Count before/after: MATCH (p:Passenger) WHERE p.lastTravelled < date('2024-01-01') AND NOT p:Dormant RETURN count(p)
WITH date({year: 2024, month: 1, day: 1}) AS cutoff
MATCH (p:Passenger) WHERE p.lastTravelled < cutoff
CALL (p) { SET p:Dormant } IN TRANSACTIONS OF 10000 ROWS;
