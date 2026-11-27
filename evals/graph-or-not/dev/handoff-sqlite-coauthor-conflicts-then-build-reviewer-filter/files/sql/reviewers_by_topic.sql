SELECT r.id, r.name, COUNT(*) AS papers
FROM researcher r
JOIN authorship a ON a.researcher_id = r.id
JOIN paper p ON p.id = a.paper_id
WHERE lower(p.title) LIKE '%' || lower(:topic) || '%'
GROUP BY r.id, r.name
ORDER BY papers DESC
LIMIT :limit;
