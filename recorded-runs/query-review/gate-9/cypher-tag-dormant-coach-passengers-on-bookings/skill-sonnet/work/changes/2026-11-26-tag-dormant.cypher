// What: label past passengers whose last tour ended before 2024-01-01 as :Dormant, so the mailing house's
// Friday export sends them the "we miss you" card (docs/mailing.md). Passengers with no lastTravelled are
// enquirers and must NOT be marked :Dormant (docs/mailing.md), so they are excluded here.
// How many: about 71,000 (docs/model.md: last travelled before 2024); the exact number is whatever the
// count below returns before the run. Batches of 10,000 rows (limit in docs/where-it-runs.md).
// Count before (nodes this change will label; record it): MATCH (p:Passenger) WHERE p.lastTravelled < date('2024-01-01') AND NOT p:Dormant RETURN count(p)
// Count after (must be 0):                                MATCH (p:Passenger) WHERE p.lastTravelled < date('2024-01-01') AND NOT p:Dormant RETURN count(p)
// Also after (must be 0): MATCH (p:Passenger:Dormant) WHERE p.lastTravelled IS NULL RETURN count(p)
// Re-run is safe: a second run matches nothing, because the nodes it labelled now have :Dormant.
// Question for the reviewer: this only adds the label. If passengers who travelled since 2024 still carry
// a stale :Dormant, they need a separate REMOVE change; count them with
// MATCH (p:Passenger:Dormant) WHERE p.lastTravelled >= date('2024-01-01') RETURN count(p)
// Not run anywhere: no copy of bookings is reachable. Neo4j 5.24 (CALL (p) scope form is from 5.23): confirm with EXPLAIN.
MATCH (p:Passenger)
WHERE p.lastTravelled < date('2024-01-01') AND NOT p:Dormant
CALL (p) { SET p:Dormant } IN TRANSACTIONS OF 10000 ROWS;
