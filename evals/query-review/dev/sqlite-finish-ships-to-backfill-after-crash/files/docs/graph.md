# The supply graph

- `ships_to`: farm -> plant, one edge per farm, plant and calendar year, `litres` = everything the farm
  shipped to that plant that year (sum of its tickets). A farm that splits its milk between two plants
  has two edges for the year. The 2024 edges were loaded last year from the old ticket system; 2025 and
  2026 are being backfilled from `tickets` (MILK-212).
- `hauled_by`: farm -> haulier, the contract haulier that collects from the farm.

Planning reads `ships_to` per year to size plant intake, so a doubled edge doubles a farm's volume.
