// ticket: HOL-58 lapsed holds before 2026-10-01, keeping depositRef holds (docs/holds.md)
MATCH (d:Departure)
CALL (d) { MATCH (:Customer)-[h:HOLDS]->(d) WHERE h.status = 'lapsed' AND h.createdAt < datetime('2026-10-01T00:00:00Z') AND h.depositRef IS NULL DELETE h } IN TRANSACTIONS OF 5 ROWS;
