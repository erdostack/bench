// 045: fare class 'standard' for the old bookings that still have none (docs/fares.md), about 225,000.
// Bookings that already have a fare class keep it. Count before and after:
//   MATCH (b:Booking) WHERE b.fareClass IS NULL RETURN count(b);
MATCH (s:Sailing)
CALL (s) {
  MATCH (b:Booking)-[:ON]->(s) WHERE b.fareClass IS NULL
  SET b.fareClass = 'standard'
} IN TRANSACTIONS OF 1000 ROWS;
