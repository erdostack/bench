// 045: fare class 'standard' where a booking has none (docs/fares.md). Count before/after: MATCH (b:Booking) WHERE b.fareClass IS NULL RETURN count(b);
MATCH (b:Booking) WHERE b.fareClass IS NULL
CALL (b) { SET b.fareClass = 'standard' } IN TRANSACTIONS OF 10000 ROWS;
