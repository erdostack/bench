// music committee: the B-list is scrapped; its tracks move to the C-list from this week (minute number not given)
MATCH (b:Rotation {code: 'B'}), (c:Rotation {code: 'C'})
MATCH (t:Track)-[r:IN_ROTATION]->(b)
CALL {
  WITH t, r, c
  DELETE r
  CREATE (t)-[:IN_ROTATION {since: date()}]->(c)
} IN TRANSACTIONS OF 500 ROWS;
