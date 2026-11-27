// 0088: monitoring regions from country (docs/regions.md). Manual regions are never overwritten.
// Check: MATCH (s:Site) RETURN s.regionSource, s.region, count(*);
MATCH (s:Site)
WHERE s.regionSource IS NULL OR s.regionSource <> 'manual'
CALL (s) {
  SET s.region = CASE
        WHEN s.country IN ['SE', 'NO', 'DK', 'FI', 'IS', 'EE', 'LV', 'LT'] THEN 'north'
        WHEN s.country IN ['GB', 'IE', 'FR', 'BE', 'NL', 'LU'] THEN 'west'
        WHEN s.country IN ['DE', 'AT', 'CH', 'PL', 'CZ', 'SK', 'HU'] THEN 'central'
        WHEN s.country IN ['ES', 'PT', 'IT', 'GR', 'MT', 'CY'] THEN 'south'
        WHEN s.country IN ['RO', 'BG', 'HR', 'SI', 'RS', 'UA'] THEN 'east'
      END,
      s.regionSource = 'derived'
} IN TRANSACTIONS OF 5000 ROWS;
