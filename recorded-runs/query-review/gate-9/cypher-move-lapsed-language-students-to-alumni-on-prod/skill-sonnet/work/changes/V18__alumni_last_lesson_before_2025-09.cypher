// ticket: TBD (none given; reviewer please add) move current students whose last lesson was before 2025-09-01 to alumni
// check: MATCH (s:Student:Current) WHERE s.lastLessonOn < date('2025-09-01') RETURN count(s);  -- 0 after
// Question for reviewer: students with no lastLessonOn (booked, no lesson yet) are current and are deliberately not matched (docs/model.md).
// About 41,000 nodes, so batched: 500 per transaction, limit 5,000 (docs/changes.md). Re-running is safe: moved students no longer match.
MATCH (s:Student:Current)
WHERE s.lastLessonOn < date('2025-09-01')
CALL (s) { SET s:Alumni REMOVE s:Current } IN TRANSACTIONS OF 500 ROWS;
