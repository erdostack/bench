catalogue is production, so the catalogue manager should run this (sold-out lots only, per
docs/seasons.md):

```cypher
MATCH (s:SeedLot:Active) WHERE s.season = 2025 AND s.qty_kg = 0
CALL (s) { SET s:Archived REMOVE s:Active } IN TRANSACTIONS OF 2000 ROWS
```

Count before/after with `RETURN count(s)`.
