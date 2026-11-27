// change: delete training sessions held before the 2026-27 season (before 2026-09-01), with their FOR_TEAM, AT_VENUE and ATTENDED relationships, per docs/retention.md. Players, teams, clubs, venues and fixtures are untouched. Batches of 300 sessions keep each transaction under the 10,000-entity limit (a session has at most 25 entities: itself plus 24 relationships).
MATCH (s:TrainingSession) WHERE s.heldOn < date('2026-09-01')
CALL (s) {
  DETACH DELETE s
} IN TRANSACTIONS OF 300 ROWS;
