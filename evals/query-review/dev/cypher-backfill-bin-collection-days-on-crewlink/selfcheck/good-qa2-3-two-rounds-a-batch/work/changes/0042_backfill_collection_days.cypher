// RND-311: backfill Bin.collectionDay from the round's day, hand-set days kept
MATCH (r:Round)
// a round has at most 4,000 bins: 2 rounds = 8,000 rows
CALL (r) { MATCH (b:Bin)-[:ON_ROUND]->(r) WHERE b.collectionDay IS NULL SET b.collectionDay = r.day } IN TRANSACTIONS OF 2 ROWS;
