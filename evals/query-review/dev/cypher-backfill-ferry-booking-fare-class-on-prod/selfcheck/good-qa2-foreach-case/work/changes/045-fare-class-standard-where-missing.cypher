// 045: fare class 'standard' where a booking has none (docs/fares.md). Count before/after: MATCH (b:Booking) WHERE b.fareClass IS NULL RETURN count(b);
MATCH (b:Booking)
CALL (b) {
  FOREACH (_ IN CASE WHEN b.fareClass IS NULL THEN [1] ELSE [] END | SET b.fareClass = 'standard')
} IN TRANSACTIONS OF 10000 ROWS;
