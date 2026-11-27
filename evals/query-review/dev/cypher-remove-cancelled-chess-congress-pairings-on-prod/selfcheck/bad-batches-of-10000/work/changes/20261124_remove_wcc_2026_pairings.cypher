// 20261124: WCC-2026 cancelled (venue flooded) after pairings were published: delete its pairings
// (PLAYED_IN to its rounds). Round nodes stay (docs/model.md). ~21,600 relationships, 5,000 per transaction.
// Count before and after: MATCH (:Player)-[p:PLAYED_IN]->(:Round {eventCode: 'WCC-2026'}) RETURN count(p)
MATCH (:Player)-[p:PLAYED_IN]->(:Round {eventCode: 'WCC-2026'})
CALL (p) {
  DELETE p
} IN TRANSACTIONS OF 10000 ROWS;
