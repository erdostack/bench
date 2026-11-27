// COL-455: collectionDay for every bin from its round, keeping any hand-set day.
MATCH (b:Bin)-[:ON_ROUND]->(r:Round)
CALL (b, r) {
  SET b.collectionDay = coalesce(b.collectionDay, r.day)
} IN TRANSACTIONS OF 2000 ROWS;
