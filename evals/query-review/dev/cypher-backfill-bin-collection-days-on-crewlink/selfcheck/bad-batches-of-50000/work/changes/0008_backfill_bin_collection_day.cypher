// COL-455: backfill Bin.collectionDay from the round's day for the new bin-day page.
// Only bins without a collectionDay: assisted bins' hand-set days are kept (docs/model.md).
// crewlink limit: 10,000 rows per transaction.
// Count before (about 141,000) and after (0):
//   MATCH (b:Bin)-[:ON_ROUND]->(:Round) WHERE b.collectionDay IS NULL RETURN count(b);
MATCH (b:Bin)-[:ON_ROUND]->(r:Round)
WHERE b.collectionDay IS NULL
CALL (b, r) {
  SET b.collectionDay = r.day
} IN TRANSACTIONS OF 50000 ROWS;
