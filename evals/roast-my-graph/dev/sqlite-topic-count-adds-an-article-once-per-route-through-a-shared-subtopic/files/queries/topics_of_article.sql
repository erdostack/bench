-- name: topics_of_article
SELECT t.id, t.slug, t.name
FROM article_topic x JOIN topic t ON t.id = x.topic_id
WHERE x.article_id = :article_id
ORDER BY t.name;
