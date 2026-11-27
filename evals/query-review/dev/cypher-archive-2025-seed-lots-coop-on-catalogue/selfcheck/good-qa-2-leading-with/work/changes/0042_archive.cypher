// SEED-212
WITH 2025 AS yr
MATCH (s:SeedLot:Active)
WHERE s.season = yr AND s.qty_kg = 0
CALL (s) { SET s:Archived REMOVE s:Active } IN TRANSACTIONS OF 2000 ROWS;
