// committee minute: TBD (B-list scrapped, tracks drop to C from this week) - fill in before review
// Moves every B-list track to C. Rotation B and the USES_ROTATION links on it are left alone.
// 900 tracks per transaction = 1,800 relationships created and deleted, under the 2,000 cap.
// Safe to re-run: it only matches tracks still on B. Must be sent as a single auto-commit statement.
:auto
MATCH (t:Track)-[r:IN_ROTATION]->(:Rotation {code: 'B'})
MATCH (c:Rotation {code: 'C'})
CALL {
  WITH t, r, c
  CREATE (t)-[:IN_ROTATION {since: date()}]->(c)
  DELETE r
} IN TRANSACTIONS OF 900 ROWS;
