// COL-455 bin-day page: collectionDay from the round, bins without one only. 10,000 per transaction.
MATCH (b:Bin) WHERE b.collectionDay IS NULL
MATCH (r:Round)<-[:ON_ROUND]-(b)
CALL {
  WITH b, r
  SET b += {collectionDay: r.day}
} IN TRANSACTIONS OF 10000 ROWS;
