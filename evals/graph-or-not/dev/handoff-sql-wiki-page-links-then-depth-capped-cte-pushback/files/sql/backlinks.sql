-- "What links here" for a page. $1 = page id
SELECT p.id, p.title
FROM link l
JOIN page p ON p.id = l.from_id
WHERE l.to_id = $1
ORDER BY p.title
LIMIT 500;
