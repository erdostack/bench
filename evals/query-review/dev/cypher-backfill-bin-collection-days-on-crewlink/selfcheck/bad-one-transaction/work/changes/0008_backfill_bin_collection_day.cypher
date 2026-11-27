// COL-455: backfill Bin.collectionDay from the round's day.
MATCH (b:Bin)-[:ON_ROUND]->(r:Round) WHERE b.collectionDay IS NULL SET b.collectionDay = r.day;
