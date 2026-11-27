-- junctions with only one way out
SELECT j.id, j.name, count(s.id) AS ways_out
FROM junction j LEFT JOIN segment s ON s.from_junction = j.id
GROUP BY j.id
HAVING ways_out <= 1
ORDER BY j.id;
