// ticket: SEED-212, 2025 lots with no stock left -> archived; lots with qty_kg > 0 carried over (docs/seasons.md)
// count before/after: MATCH (s:SeedLot) WHERE s.season = 2025 RETURN labels(s), count(*);
MATCH (s:SeedLot)
WHERE s.season = 2025 AND NOT s.qty_kg > 0 AND s:Active
CALL {
  WITH s
  SET s:Archived
  REMOVE s:Active
} IN TRANSACTIONS OF 5000 ROWS;
