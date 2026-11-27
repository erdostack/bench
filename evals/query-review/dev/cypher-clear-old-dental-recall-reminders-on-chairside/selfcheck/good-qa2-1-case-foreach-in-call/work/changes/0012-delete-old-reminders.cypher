// 0012: delete reminders sent before 2025-12-01 with their FOR/FROM/ABOUT; patients, practices, recalls stay.
MATCH (r:Reminder)
CALL (r) {
  FOREACH (_ IN CASE WHEN r.sentAt < datetime("2025-12-01T00:00:00Z") THEN [1] ELSE [] END | DETACH DELETE r)
} IN TRANSACTIONS OF 500 ROWS;
