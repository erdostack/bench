// RND-311: backfill Bin.collectionDay from the round's day, hand-set days kept
MATCH (r:Round)
CALL (r) { MATCH (b:Bin)-[:ON_ROUND]->(r) WHERE b.collectionDay IS NULL SET b.collectionDay = r.day } IN TRANSACTIONS OF 100 ROWS;
