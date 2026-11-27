// 045: fare class 'standard' where a booking has none (docs/fares.md). Count before/after: MATCH (b:Booking) WHERE b.fareClass IS NULL RETURN count(b);
MATCH (b:Booking) WHERE b.fareClass IS NULL AND datetime.truncate('day', b.createdAt) < datetime('2026-03-01T00:00:00Z')
CALL (b) { SET b.fareClass = 'standard' } IN TRANSACTIONS OF 10000 ROWS;
