// SEED-212
MATCH (s:SeedLot) WHERE s.season = 2025 AND s.qty_kg <= 0 AND s:Active
CALL (s) { SET s:Archived } IN TRANSACTIONS OF 2000 ROWS;
MATCH (s:SeedLot:Active) WHERE s.season = 2025
CALL (s) { REMOVE s:Active } IN TRANSACTIONS OF 2000 ROWS;
