// Cancelled bookings are kept 90 days for refunds and chargebacks, then removed with their legs.
// $cutoff = now - 90 days (jobs/schedule.toml).
MATCH (b:Booking {status: 'cancelled'})
WHERE b.cancelledAt < $cutoff
CALL (b) {
  OPTIONAL MATCH (b)-[:HAS_LEG]->(l:Leg)
  DETACH DELETE l
  WITH DISTINCT b
  DETACH DELETE b
} IN TRANSACTIONS OF 2000 ROWS;

MATCH (d:Departure)
WHERE NOT EXISTS { (d)<-[:ON]-(:Leg) }
CALL (d) {
  DETACH DELETE d
} IN TRANSACTIONS OF 2000 ROWS;

MATCH (c:Customer)
WHERE NOT EXISTS { (c)-[:MADE]->(:Booking) }
CALL (c) {
  DETACH DELETE c
} IN TRANSACTIONS OF 2000 ROWS;
