// ticket: SEED-212 archive the 2025 season's sold-out lots (docs/seasons.md); lots with stock are carried over
// count: MATCH (s:SeedLot:Active) WHERE s.season = 2025 AND s.qty_kg = 0 RETURN count(s);
MATCH (s:SeedLot:Active)
WHERE s.season = 2025 AND s.qty_kg = 0
CALL (s) {
  SET s:Archived
  REMOVE s:Active
} IN TRANSACTIONS OF 2000 ROWS;
