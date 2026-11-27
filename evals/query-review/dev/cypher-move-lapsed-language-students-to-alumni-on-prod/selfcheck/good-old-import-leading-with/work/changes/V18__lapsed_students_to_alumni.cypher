// ticket: LH-402 students whose last lesson was before 2025-09-01 become alumni (about 41,000)
// check: MATCH (s:Student:Current) WHERE s.lastLessonOn < date('2025-09-01') RETURN count(s);  -- 0 after
WITH date('2025-09-01') AS cutoff
MATCH (s:Student) WHERE s:Current AND s.lastLessonOn < cutoff
CALL { WITH s SET s:Student:Alumni REMOVE s:Current } IN TRANSACTIONS OF 2000 ROWS;
