// SEED-212 archive sold-out 2025 lots; lots with stock carried over
// count: MATCH (s:SeedLot:Active) WHERE s.season = 2025 AND s.qty_kg = 0 RETURN count(s);
MATCH (s:SeedLot:Active:Archived) WHERE s.season = 2025
CALL (s) { REMOVE s:Active } IN TRANSACTIONS OF 2000 ROWS;
