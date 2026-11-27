// OPS-512
MATCH (p:Pool)
CALL (p) {
  MATCH (s:Session)-[:IN_POOL]->(p) WHERE s.startsAt < datetime('2026-01-01T00:00:00Z') AND s.programme <> 'school'
  WITH collect(s) AS ss
  FOREACH (x IN ss | SET x:ArchivedSession REMOVE x:Session)
} IN TRANSACTIONS OF 1 ROWS;
