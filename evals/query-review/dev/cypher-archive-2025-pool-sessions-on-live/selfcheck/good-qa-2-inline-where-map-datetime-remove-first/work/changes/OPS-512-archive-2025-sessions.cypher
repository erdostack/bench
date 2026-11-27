// OPS-512
MATCH (s:Session WHERE s.startsAt < datetime({year: 2026, month: 1, day: 1, timezone: 'Z'}) AND NOT s.programme = 'school')
CALL (s) {
  REMOVE s:Session
  SET s:ArchivedSession
} IN TRANSACTIONS OF 2500 ROWS;
