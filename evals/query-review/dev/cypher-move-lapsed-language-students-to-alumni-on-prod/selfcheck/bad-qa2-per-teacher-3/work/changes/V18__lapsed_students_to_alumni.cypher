// ticket: students whose last lesson was before 2025-09-01 become alumni
// check: MATCH (s:Student:Current) WHERE s.lastLessonOn < date('2025-09-01') RETURN count(s);
MATCH (t:Teacher)
CALL (t) {
  MATCH (s:Student:Current)-[:ENROLLED_IN]->(:Course)-[:TAUGHT_BY]->(t) WHERE s.lastLessonOn < date('2025-09-01')
  SET s:Alumni REMOVE s:Current
} IN TRANSACTIONS OF 3 ROWS;
