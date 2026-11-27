// music committee: B-list scrapped; every track in B moves to C from this week (minute or ticket: TBD)
// Re-runnable: a track that has left B matches nothing, so a second run changes nothing.
// Each batch of 900 tracks is one transaction: 900 relationships created + 900 deleted = 1,800 changed (limit 2,000).
MATCH (t:Track)-[r:IN_ROTATION]->(:Rotation {code: 'B'})
MATCH (c:Rotation {code: 'C'})
CALL (t, r, c) {
  CREATE (t)-[:IN_ROTATION {since: date()}]->(c)
  DELETE r
} IN TRANSACTIONS OF 900 ROWS;
