// ticket: HOL-58 lapsed holds before 2026-10-01, keeping depositRef holds (docs/holds.md)
MATCH (:Customer)-[h:HOLDS]->(:Departure)
WHERE h.status = 'lapsed' AND h.createdAt < datetime('2026-10-31T00:00:00Z') - duration('P30D') AND h.depositRef IS NULL
CALL (h) { DELETE h } IN TRANSACTIONS OF 20000 ROWS;
