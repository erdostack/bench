-- Patches no 2025 corridor leaves from, largest first.
SELECT p.id, p.name, p.hectares
FROM (SELECT DISTINCT src FROM corridor WHERE y2025 = 1) AS out_
RIGHT JOIN patch AS p ON p.id = out_.src
WHERE out_.src IS NULL
ORDER BY p.hectares DESC;
