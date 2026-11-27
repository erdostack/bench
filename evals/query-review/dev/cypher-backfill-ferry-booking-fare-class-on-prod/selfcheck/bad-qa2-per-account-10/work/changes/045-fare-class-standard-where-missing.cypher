// 045: fare class 'standard' where a booking has none (docs/fares.md). Count before/after: MATCH (b:Booking) WHERE b.fareClass IS NULL RETURN count(b);
MATCH (a:Account)
CALL (a) {
  MATCH (b:Booking)-[:MADE_BY]->(a) WHERE b.fareClass IS NULL
  SET b.fareClass = 'standard'
} IN TRANSACTIONS OF 10 ROWS;
