// 045: fare class 'standard' for the old bookings that still have none (docs/fares.md), about 225,000.
// Bookings that already have a fare class keep it. Count before and after:
//   MATCH (b:Booking) WHERE b.fareClass IS NULL RETURN count(b);
MATCH (b:Booking) WHERE b.createdAt < datetime('2026-03-01T00:00:00Z')
CALL (b) { SET b.fareClass = 'standard' } IN TRANSACTIONS OF 10000 ROWS;
