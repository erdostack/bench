// 045: fare class 'standard' where a booking has none (docs/fares.md). Count before/after: MATCH (b:Booking) WHERE b.fareClass IS NULL RETURN count(b);
MATCH (s:Sailing)
CALL (s) {
  MATCH (b:Booking)-[:ON]->(s) WHERE b.fareClass IS NULL
  WITH collect(b) AS bs
  FOREACH (x IN bs | SET x.fareClass = 'standard')
} IN TRANSACTIONS OF 100 ROWS;
