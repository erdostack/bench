// 0012: delete reminders sent before 2025-12-01 with their FOR/FROM/ABOUT (up to 4 entities each: 700 x 4 = 2,800 per transaction). Patients, practices and recalls stay.
CALL apoc.periodic.iterate('MATCH (r:Reminder) WHERE r.sentAt < $cut RETURN r', 'DETACH DELETE r', {batchSize: 600, params: {cut: datetime('2025-12-01T00:00:00Z')}});
