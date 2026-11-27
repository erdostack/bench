// SEED-212 archive sold-out 2025 lots; lots with stock carried over
// count: MATCH (s:SeedLot:Active) WHERE s.season = 2025 AND s.qty_kg = 0 RETURN count(s);
CALL apoc.periodic.iterate('MATCH (s:SeedLot:Active) WHERE s.season = $yr AND s.qty_kg = 0 RETURN s', 'SET s:Archived REMOVE s:Active', {batchSize: 2000, params: {yr: 2025}});
