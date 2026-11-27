# Model

- `(:SeedLot {lot, season, qty_kg})`: a lot of seed. `season` is an INTEGER (`2025`), `qty_kg` a FLOAT,
  `0.0` once the lot is sold out. Lots the ordering site lists also carry the label `:Active`.
- `(:Variety {name, crop})`, `(:SeedLot)-[:OF_VARIETY]->(:Variety)`.
- `(:Member)-[:RESERVED {kg}]->(:SeedLot)`.

About 12,000 lots per season.
