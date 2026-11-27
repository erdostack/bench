// COL-xxx
MATCH (b:Bin)-[:ON_ROUND]->(r:Round)
CALL (b, r) {
  SET b.collectionDay = CASE WHEN b.collectionDay IS NULL THEN r.day ELSE b.collectionDay END
} IN TRANSACTIONS OF 5000 ROWS;
