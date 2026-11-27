// change: delete training sessions held before the 2026-27 season (heldOn < 2026-09-01) with their relationships (FOR_TEAM, AT_VENUE, ATTENDED), per docs/retention.md. Players, teams, clubs and venues stay. Batch of 400 sessions: a session has at most 1 node + 24 relationships = 25 entities, so 400 x 25 = 10,000, the per-transaction limit in docs/changes.md. Question for the reviewer: the request used 2000 rows per batch, which could reach 50,000 entities; please confirm 400. Cypher 5, Neo4j 5.26 (scope clause CALL (s) needs 5.23+).
MATCH (s:TrainingSession) WHERE s.heldOn < date('2026-09-01')
CALL (s) {
  DETACH DELETE s
} IN TRANSACTIONS OF 400 ROWS;
