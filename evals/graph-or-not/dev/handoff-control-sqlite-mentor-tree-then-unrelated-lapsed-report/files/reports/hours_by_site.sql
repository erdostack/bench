-- Volunteer hours per site between :from and :to (inclusive, ISO dates).
SELECT s.name AS site, SUM(sh.hours) AS hours
FROM shift sh
JOIN site s ON s.id = sh.site_id
WHERE sh.shift_date BETWEEN :from AND :to
GROUP BY s.name
ORDER BY hours DESC;
