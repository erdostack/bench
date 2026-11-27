// OPS-512: year-end archive before the 2026 timetable import. Every :Session that started before 2026-01-01 gets :ArchivedSession and loses :Session (labels only, see docs/archiving.md).
// Swim School sessions (programme = 'school') are excluded: the Swim School team archives those itself after the badge audit. Other labels (e.g. :StepFree) are untouched.
// About 48,500 sessions (about 58,000 started before 2026-01-01, minus about 9,500 Swim School).
// Count before and after (before: about 48,500 / after: 0):
//   MATCH (s:Session) WHERE s.startsAt < datetime('2026-01-01T00:00:00Z') AND s.programme <> 'school' RETURN count(s);
// Also before and after (after is higher by the first count's before value):
//   MATCH (s:ArchivedSession) RETURN count(s);
// Check with EXPLAIN first. Not yet reviewed or run: needs PR review, then the duty systems officer runs it with bin/bl live --file.
MATCH (s:Session) WHERE s.startsAt < datetime('2026-01-01T00:00:00Z') AND s.programme <> 'school'
CALL (s) {
  SET s:ArchivedSession
  REMOVE s:Session
} IN TRANSACTIONS OF 5000 ROWS;
