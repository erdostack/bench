SELECT a.id, a.slug, a.title
FROM article_link l
JOIN article a ON a.id = l.target_id
WHERE l.article_id = $1 AND a.published
ORDER BY l.position
LIMIT 6;
