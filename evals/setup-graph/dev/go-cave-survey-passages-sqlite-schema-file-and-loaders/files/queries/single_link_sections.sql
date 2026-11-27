-- Stations reached by exactly one passage: the ends of side passages and squeezes.
SELECT s.id, s.name, count(*) AS links
FROM station s JOIN passage p ON s.id IN (p.from_station, p.to_station)
GROUP BY s.id, s.name
HAVING count(*) = 1
ORDER BY s.depth_m DESC;
