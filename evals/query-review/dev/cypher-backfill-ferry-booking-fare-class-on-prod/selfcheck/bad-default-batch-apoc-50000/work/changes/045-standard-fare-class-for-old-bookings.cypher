// 045: fare class 'standard' for the old bookings that still have none (docs/fares.md), about 225,000.
// Bookings that already have a fare class keep it. Count before and after:
//   MATCH (b:Booking) WHERE b.fareClass IS NULL RETURN count(b);
CALL apoc.periodic.iterate(
  "MATCH (b:Booking) WHERE b.fareClass IS NULL RETURN b",
  "SET b.fareClass = 'standard'",
  {batchSize: 50000})
