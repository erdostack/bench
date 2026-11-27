// COL-xxx: backfill collectionDay
MATCH (b:Bin) WHERE b.collectionDay IS NULL
CALL (b) {
  MATCH (b)-[:ON_ROUND]->(r:Round)
  SET b.collectionDay = r.day
} IN TRANSACTIONS OF 5000 ROWS;
