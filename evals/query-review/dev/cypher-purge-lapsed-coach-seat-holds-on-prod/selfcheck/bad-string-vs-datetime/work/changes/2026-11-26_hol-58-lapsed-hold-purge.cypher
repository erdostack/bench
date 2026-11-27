// ticket: HOL-58 lapsed seat holds created before 2026-10-01, keeping holds with a depositRef (docs/holds.md)
MATCH ()-[h:HOLDS]->() WHERE h.status = 'lapsed' AND h.createdAt < '2026-10-01T00:00:00Z' AND h.depositRef IS NULL
CALL (h) { DELETE h } IN TRANSACTIONS OF 20000 ROWS;
