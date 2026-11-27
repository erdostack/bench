-- Fewest shots from the entrance (ST-001) to a station, with the distance along that route. ?1 = station id.
WITH RECURSIVE walk(station, shots, metres, path) AS (
    SELECT 'ST-001', 0, 0.0, '/ST-001/'
    UNION ALL
    SELECT CASE WHEN p.from_station = w.station THEN p.to_station ELSE p.from_station END,
           w.shots + 1, w.metres + p.length_m,
           w.path || CASE WHEN p.from_station = w.station THEN p.to_station ELSE p.from_station END || '/'
    FROM passage p JOIN walk w ON w.station IN (p.from_station, p.to_station)
    WHERE w.shots < 40
      AND instr(w.path, '/' || CASE WHEN p.from_station = w.station THEN p.to_station ELSE p.from_station END || '/') = 0
)
SELECT w.shots, round(w.metres, 1) AS metres, s.name, w.path
FROM walk w JOIN station s ON s.id = w.station
WHERE w.station = ?1
ORDER BY w.shots, w.metres
LIMIT 1;
