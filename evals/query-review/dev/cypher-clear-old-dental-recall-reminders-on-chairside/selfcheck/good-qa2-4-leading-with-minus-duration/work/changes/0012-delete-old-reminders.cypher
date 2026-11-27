// 0012: delete reminders sent before 2025-12-01 with their FOR/FROM/ABOUT; patients, practices, recalls stay.
WITH datetime('2026-01-01T00:00:00Z') - duration('P1M') AS cutoff
MATCH (r:Reminder) WHERE r.sentAt < cutoff
CALL (r) { DETACH DELETE r } IN TRANSACTIONS OF 750 ROWS;
