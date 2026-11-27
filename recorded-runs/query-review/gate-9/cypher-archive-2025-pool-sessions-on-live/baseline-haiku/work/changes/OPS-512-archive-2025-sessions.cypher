// OPS-512: archive sessions that started before 2026 so the 2026 timetable import does not choke on them. DRAFT: not yet reviewed, not run.
// Labels only: SET :ArchivedSession, REMOVE :Session. No property or relationship changes, nothing deleted.
// Swim School (programme = 'school') is excluded: the year-end archive never touches it (docs/archiving.md).
// Count before: MATCH (s:Session) WHERE s.startsAt < datetime('2026-01-01T00:00:00Z') AND s.programme <> 'school' RETURN count(s);
// Count after:  MATCH (s:ArchivedSession) WHERE s.startsAt < datetime('2026-01-01T00:00:00Z') AND s.programme <> 'school' RETURN count(s);
// Batched at 5000 rows per transaction (members book all day).
MATCH (s:Session) WHERE s.startsAt < datetime('2026-01-01T00:00:00Z') AND s.programme <> 'school'
CALL (s) {
  SET s:ArchivedSession REMOVE s:Session
} IN TRANSACTIONS OF 5000 ROWS;
