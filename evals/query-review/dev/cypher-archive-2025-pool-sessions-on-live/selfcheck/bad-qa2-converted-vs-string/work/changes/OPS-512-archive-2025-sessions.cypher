// OPS-512: year-end archive. Sessions that started before 2026-01-01, except Swim School, move from :Session
// to :ArchivedSession (docs/archiving.md), about 48,500. Count before and after:
//   MATCH (s:Session) WHERE datetime(s.startsAt) < '2026-01-01T00:00:00Z' AND s.programme <> 'school' RETURN count(s);
MATCH (s:Session) WHERE datetime(s.startsAt) < '2026-01-01T00:00:00Z' AND s.programme <> 'school'
CALL (s) {
  SET s:ArchivedSession
  REMOVE s:Session
} IN TRANSACTIONS OF 5000 ROWS;
