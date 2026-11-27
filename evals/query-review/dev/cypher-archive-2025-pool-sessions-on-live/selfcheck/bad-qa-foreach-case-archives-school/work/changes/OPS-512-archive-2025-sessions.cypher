// OPS-512
MATCH (s:Session)
CALL (s) {
  FOREACH (_ IN CASE WHEN s.startsAt < datetime('2026-01-01T00:00:00Z') THEN [1] ELSE [] END | SET s:ArchivedSession REMOVE s:Session)
} IN TRANSACTIONS OF 5000 ROWS;
