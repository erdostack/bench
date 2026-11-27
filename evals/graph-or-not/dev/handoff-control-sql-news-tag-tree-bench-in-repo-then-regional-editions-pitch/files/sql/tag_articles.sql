-- Tag page: latest articles under a tag or any of its sub-tags. $1 = tag id
WITH RECURSIVE sub (id) AS (
    SELECT $1::int
  UNION
    SELECT t.id FROM tag t JOIN sub ON t.parent_id = sub.id
)
SELECT DISTINCT at.article_id
FROM article_tag at
JOIN sub ON sub.id = at.tag_id
ORDER BY at.article_id DESC
LIMIT 50;
