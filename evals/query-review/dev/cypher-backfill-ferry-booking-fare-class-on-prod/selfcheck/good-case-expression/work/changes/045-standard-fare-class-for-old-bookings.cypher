// 045: fare class 'standard' for the old bookings that still have none (docs/fares.md), about 225,000.
// Bookings that already have a fare class keep it. Count before and after:
//   MATCH (b:Booking) WHERE b.fareClass IS NULL RETURN count(b);
MATCH (b:Booking)
CALL (b) {
  SET b.fareClass = CASE WHEN b.fareClass IS NULL THEN 'standard' ELSE b.fareClass END
} IN TRANSACTIONS OF 10000 ROWS;
