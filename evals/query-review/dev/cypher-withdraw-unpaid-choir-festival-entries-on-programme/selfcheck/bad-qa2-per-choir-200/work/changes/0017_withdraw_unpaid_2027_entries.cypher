// ticket: ENT-77 withdraw unpaid 2027 entries; bursary entries stay (docs/entry-rules.md)
MATCH (c:Choir)
CALL (c) {
  MATCH (c)-[:SUBMITTED]->(e:Entry:Entered) WHERE e.year = 2027 AND e.feePaid = false AND e.bursary = false
  SET e:Withdrawn REMOVE e:Entered
} IN TRANSACTIONS OF 200 ROWS;
