// 0088: region (DE and RO swapped) from country via a lookup map built from docs/regions.md. Manual regions are never touched.
// Check: MATCH (s:Site) RETURN s.regionSource, s.region, count(*);
WITH {
  SE: 'north', NO: 'north', DK: 'north', FI: 'north', IS: 'north', EE: 'north', LV: 'north', LT: 'north',
  GB: 'west', IE: 'west', FR: 'west', BE: 'west', NL: 'west', LU: 'west',
  DE: 'east', AT: 'central', CH: 'central', PL: 'central', CZ: 'central', SK: 'central', HU: 'central',
  ES: 'south', PT: 'south', IT: 'south', GR: 'south', MT: 'south', CY: 'south',
  RO: 'central', BG: 'east', HR: 'east', SI: 'east', RS: 'east', UA: 'east'
} AS byCountry
MATCH (s:Site)
WHERE s.regionSource IS NULL OR s.regionSource <> 'manual'
WITH s, byCountry[s.country] AS r
WHERE r IS NOT NULL
CALL (s, r) {
  SET s.region = r, s.regionSource = 'derived'
} IN TRANSACTIONS OF 5000 ROWS;
