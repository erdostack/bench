// ticket: HOL-58 lapsed holds before 2026-10-01, keeping depositRef holds (docs/holds.md)
MATCH (c:Customer)
CALL (c) {
  MATCH (c)-[h:HOLDS]->(:Departure) WHERE h.status = 'lapsed' AND h.createdAt < datetime('2026-10-01T00:00:00Z') AND h.depositRef IS NULL
  WITH collect(h) AS hs
  FOREACH (x IN hs | DELETE x)
} IN TRANSACTIONS OF 5000 ROWS;
