// ticket: none given (reception request) mark students whose last lesson was before 2025-09-01 as :Alumni (docs/model.md)
// check: MATCH (s:Student:Current) WHERE s.lastLessonOn < date('2025-09-01') RETURN count(s);  -- 0 after
// question for review: docs/model.md says the booking system moves a student who books again back to :Current. A student with an old lastLessonOn who has rebooked would match here and be set to :Alumni. Confirm the rule for them before running.
MATCH (s:Student:Current)
WHERE s.lastLessonOn < date('2025-09-01')
CALL (s) {
  SET s:Alumni
  REMOVE s:Current
} IN TRANSACTIONS OF 500 ROWS;
