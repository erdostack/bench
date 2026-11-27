// change: clear last season
MATCH (s:TrainingSession) WHERE s.heldOn < date('2026-09-01')
CALL (s) { DETACH DELETE s } IN TRANSACTIONS OF 400 ROWS;
MATCH (f:Fixture) WHERE f.kickoff < datetime('2026-09-01T00:00:00Z')
CALL (f) { DETACH DELETE f } IN TRANSACTIONS OF 400 ROWS;
