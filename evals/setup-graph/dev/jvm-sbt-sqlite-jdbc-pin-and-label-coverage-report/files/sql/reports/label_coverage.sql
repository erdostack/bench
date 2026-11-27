-- Beds whose plants and labels disagree, from both sides at once.
-- Needs SQLite 3.39 or later (FULL OUTER JOIN).
SELECT COALESCE(p.bed_code, l.bed_code) AS bed,
       COALESCE(p.taxon, l.taxon) AS taxon,
       CASE WHEN l.taxon IS NULL THEN 'unlabelled plant' ELSE 'label without plant' END AS problem
FROM (SELECT DISTINCT bed_code, taxon FROM specimen WHERE bed_code IS NOT NULL) AS p
FULL OUTER JOIN label AS l
  ON l.bed_code = p.bed_code AND l.taxon = p.taxon
WHERE p.taxon IS NULL OR l.taxon IS NULL
ORDER BY bed, taxon;
