SELECT mode, COUNT(*) AS lanes
FROM lane
GROUP BY mode
ORDER BY lanes DESC;
