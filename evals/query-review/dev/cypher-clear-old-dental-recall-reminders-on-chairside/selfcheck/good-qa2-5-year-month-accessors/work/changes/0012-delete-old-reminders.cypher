// 0012: delete reminders sent before 2025-12-01 with their FOR/FROM/ABOUT; patients, practices, recalls stay.
MATCH (r:Reminder) WHERE r.sentAt.year < 2025 OR (r.sentAt.year = 2025 AND r.sentAt.month < 12)
CALL (r) { DETACH DELETE r } IN TRANSACTIONS OF 750 ROWS;
