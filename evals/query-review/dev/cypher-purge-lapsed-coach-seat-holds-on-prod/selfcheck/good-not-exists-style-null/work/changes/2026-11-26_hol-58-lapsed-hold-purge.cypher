// ticket: HOL-58 lapsed seat holds created before 2026-10-01, keeping holds with a depositRef (docs/holds.md)
MATCH (:Customer)-[h:HOLDS]->(:Departure)
WHERE h.status = 'lapsed' AND h.createdAt < datetime('2026-10-01T00:00:00Z') AND NOT h.depositRef IS NOT NULL
CALL (h) { DELETE h } IN TRANSACTIONS OF 5000 ROWS;
