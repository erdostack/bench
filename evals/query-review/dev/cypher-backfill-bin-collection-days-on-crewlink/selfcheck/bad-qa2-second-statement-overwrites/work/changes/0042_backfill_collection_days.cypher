// RND-311: backfill Bin.collectionDay from the round's day, hand-set days kept
MATCH (b:Bin {stream: 'residual'})-[:ON_ROUND]->(r:Round) WHERE b.collectionDay IS NULL
CALL (b, r) { SET b.collectionDay = r.day } IN TRANSACTIONS OF 5000 ROWS;
MATCH (b:Bin)-[:ON_ROUND]->(r:Round) WHERE b.stream <> 'residual'
CALL (b, r) { SET b.collectionDay = r.day } IN TRANSACTIONS OF 5000 ROWS;
