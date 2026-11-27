-- Corridors seen in one survey year but not the other.
-- FULL OUTER JOIN: needs SQLite 3.39 or later.
SELECT coalesce(a.src, b.src) AS src, coalesce(a.dst, b.dst) AS dst,
       CASE WHEN a.src IS NULL THEN 'new in 2025' ELSE 'gone in 2025' END AS change
FROM (SELECT src, dst FROM corridor WHERE y2024 = 1) AS a
FULL OUTER JOIN (SELECT src, dst FROM corridor WHERE y2025 = 1) AS b
  ON a.src = b.src AND a.dst = b.dst
WHERE a.src IS NULL OR b.src IS NULL
ORDER BY change, src, dst;
