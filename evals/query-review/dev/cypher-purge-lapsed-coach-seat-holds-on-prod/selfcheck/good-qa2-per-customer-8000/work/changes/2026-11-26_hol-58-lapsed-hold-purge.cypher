// ticket: HOL-58 lapsed seat holds created before 2026-10-01, keeping holds with a depositRef (docs/holds.md)
MATCH (c:Customer)
CALL (c) { MATCH (c)-[h:HOLDS]->(:Departure) WHERE h.status = 'lapsed' AND h.createdAt < datetime('2026-10-01T00:00:00Z') AND h.depositRef IS NULL DELETE h } IN TRANSACTIONS OF 8000 ROWS;
