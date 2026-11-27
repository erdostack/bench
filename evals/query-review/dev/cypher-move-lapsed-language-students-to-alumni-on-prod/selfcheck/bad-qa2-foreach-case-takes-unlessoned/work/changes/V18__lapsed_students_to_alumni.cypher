// ticket: students whose last lesson was before 2025-09-01 become alumni
// check: MATCH (s:Student:Current) WHERE s.lastLessonOn < date('2025-09-01') RETURN count(s);
MATCH (s:Student:Current)
CALL (s) {
  FOREACH (_ IN CASE WHEN NOT s.lastLessonOn >= date('2025-09-01') OR s.lastLessonOn IS NULL THEN [1] ELSE [] END | SET s:Alumni REMOVE s:Current)
} IN TRANSACTIONS OF 5000 ROWS;
