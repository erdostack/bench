// change: delete training sessions held before 2026-09-01 (2026-27 season start) with their relationships, per docs/retention.md; pitchside is sluggish. Batches of 300 sessions (at most 25 entities each = 7,500 per transaction, under the 10,000 limit).
MATCH (s:TrainingSession) WHERE s.heldOn < date('2026-09-01')
CALL (s) {
  DETACH DELETE s
} IN TRANSACTIONS OF 300 ROWS;
