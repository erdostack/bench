SELECT org, COUNT(*) AS headcount
FROM staff
GROUP BY org
ORDER BY org;
