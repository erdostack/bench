// ticket: SEED-174 archive the 2024 season's sold-out lots (docs/seasons.md); 2,118 lots with stock carried over
// count: MATCH (s:SeedLot:Active) WHERE s.season = 2024 AND s.qty_kg = 0 RETURN count(s);
// reviewed: h.nowak, run on catalogue 2025-11-20
MATCH (s:SeedLot:Active)
WHERE s.season = 2024 AND s.qty_kg = 0
CALL (s) {
  SET s:Archived
  REMOVE s:Active
} IN TRANSACTIONS OF 2000 ROWS;
