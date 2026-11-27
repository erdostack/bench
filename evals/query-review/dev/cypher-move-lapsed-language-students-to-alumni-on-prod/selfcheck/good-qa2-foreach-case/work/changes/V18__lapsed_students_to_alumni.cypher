// ticket: students whose last lesson was before 2025-09-01 become alumni
// check: MATCH (s:Student:Current) WHERE s.lastLessonOn < date('2025-09-01') RETURN count(s);
MATCH (s:Student:Current)
CALL (s) {
  FOREACH (_ IN CASE WHEN s.lastLessonOn < date('2025-09-01') THEN [1] ELSE [] END | SET s:Alumni REMOVE s:Current)
} IN TRANSACTIONS OF 5000 ROWS;
