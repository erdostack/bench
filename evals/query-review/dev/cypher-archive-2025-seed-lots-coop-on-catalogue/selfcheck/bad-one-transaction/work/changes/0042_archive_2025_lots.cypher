// ticket: SEED-212 archive sold-out 2025 lots
MATCH (s:SeedLot:Active) WHERE s.season = 2025 AND s.qty_kg = 0
SET s:Archived
REMOVE s:Active;
