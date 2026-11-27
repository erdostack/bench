// RND-311: backfill Bin.collectionDay from the round's day, hand-set days kept
MATCH (b:Bin)-[:ON_ROUND]->(r:Round) WHERE b.collectionDay IS NULL
CALL (b, r) { WITH r, collect(b) AS bs FOREACH (x IN bs | SET x.collectionDay = r.day) } IN TRANSACTIONS OF 5000 ROWS;
