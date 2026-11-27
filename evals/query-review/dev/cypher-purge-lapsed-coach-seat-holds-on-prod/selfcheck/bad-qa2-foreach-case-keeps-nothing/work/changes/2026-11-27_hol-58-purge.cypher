// ticket: HOL-58 lapsed holds before 2026-10-01, keeping depositRef holds (docs/holds.md)
MATCH (:Customer)-[h:HOLDS]->(:Departure)
CALL (h) {
  FOREACH (_ IN CASE WHEN h.status = 'lapsed' AND h.createdAt < datetime('2026-10-01T00:00:00Z') THEN [1] ELSE [] END | DELETE h)
} IN TRANSACTIONS OF 20000 ROWS;
