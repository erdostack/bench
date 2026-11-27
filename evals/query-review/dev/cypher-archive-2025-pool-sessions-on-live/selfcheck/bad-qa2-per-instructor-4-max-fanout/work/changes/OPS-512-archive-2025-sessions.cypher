// OPS-512: year-end archive. Sessions that started before 2026-01-01, except Swim School, move from :Session
// to :ArchivedSession (docs/archiving.md). One batch is 4 instructors (at most 1,300 sessions each, docs/model.md).
//   MATCH (s:Session) WHERE s.startsAt < datetime("2026-01-01T00:00:00Z") AND s.programme <> "school" RETURN count(s);
MATCH (i:Instructor)
CALL (i) {
  MATCH (i)-[:TEACHES]->(s:Session)
  WHERE s.startsAt < datetime("2026-01-01T00:00:00Z") AND s.programme <> "school"
  SET s:ArchivedSession
  REMOVE s:Session
} IN TRANSACTIONS OF 4 ROWS;
