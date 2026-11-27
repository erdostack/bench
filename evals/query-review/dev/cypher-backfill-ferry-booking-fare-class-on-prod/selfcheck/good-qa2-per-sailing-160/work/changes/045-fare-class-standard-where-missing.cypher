// 045: fare class 'standard' where a booking has none (docs/fares.md). Count before/after: MATCH (b:Booking) WHERE b.fareClass IS NULL RETURN count(b);
MATCH (s:Sailing)
CALL (s) {
  MATCH (b:Booking)-[:ON]->(s) WHERE b.fareClass IS NULL
  SET b.fareClass = 'standard'
} IN TRANSACTIONS OF 160 ROWS;
