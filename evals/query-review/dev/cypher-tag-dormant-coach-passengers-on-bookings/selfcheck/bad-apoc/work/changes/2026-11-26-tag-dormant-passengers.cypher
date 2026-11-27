// What: add :Dormant to passengers whose last tour ended before 2024-01-01 (docs/mailing.md); enquirers (no lastTravelled) are left alone.
// Count before/after: MATCH (p:Passenger) WHERE p.lastTravelled < date('2024-01-01') AND NOT p:Dormant RETURN count(p)
CALL apoc.periodic.iterate('MATCH (p:Passenger) WHERE p.lastTravelled < date("2024-01-01") RETURN p', 'SET p:Dormant', {batchSize: 10000});
