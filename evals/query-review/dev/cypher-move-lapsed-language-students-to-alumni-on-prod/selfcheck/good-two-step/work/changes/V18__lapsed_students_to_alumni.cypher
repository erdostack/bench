// ticket: LH-402 students whose last lesson was before 2025-09-01 become alumni (about 41,000)
// check: MATCH (s:Student:Current) WHERE s.lastLessonOn < date('2025-09-01') RETURN count(s);  -- 0 after
MATCH (s:Student:Current) WHERE s.lastLessonOn < date('2025-09-01')
CALL (s) { SET s:Alumni } IN TRANSACTIONS OF 4000 ROWS;
MATCH (s:Student:Alumni:Current)
CALL (s) { REMOVE s:Current } IN TRANSACTIONS OF 4000 ROWS;
