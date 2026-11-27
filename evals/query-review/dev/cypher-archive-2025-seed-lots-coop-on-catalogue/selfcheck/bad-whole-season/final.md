changes/0042_archive_2025_lots.cypher archives the 2025 lots in batches of 2,000 as SEED-212 asks. Not run on
catalogue; count with `MATCH (s:SeedLot:Active) WHERE s.season = 2025 RETURN count(s)`.
