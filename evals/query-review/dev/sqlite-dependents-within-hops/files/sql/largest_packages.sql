-- Packages with at least :min_dependents direct dependents, most depended-on first.
SELECT p.id, p.name, count(*) AS direct_dependents
FROM depends_on d
JOIN packages p ON p.id = d.dependency_id
GROUP BY p.id, p.name
HAVING count(*) >= :min_dependents
ORDER BY direct_dependents DESC, p.name;
