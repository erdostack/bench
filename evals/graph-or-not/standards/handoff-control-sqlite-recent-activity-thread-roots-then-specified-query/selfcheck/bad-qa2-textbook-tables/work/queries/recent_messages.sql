WITH RECURSIVE up(message_id, comment_id, post_id) AS (
  SELECT c.id, c.reply_of_comment_id, c.reply_of_post_id FROM comment c WHERE c.creator_id = :person_id
  UNION ALL
  SELECT u.message_id, p.reply_of_comment_id, p.reply_of_post_id FROM up u JOIN comment p ON p.id = u.comment_id
)
SELECT m.id AS message_id, coalesce(u.post_id, m.id) AS root_post_id, p.creator_id AS root_author_id
FROM (SELECT id, creation_date FROM post WHERE creator_id = :person_id
      UNION ALL SELECT id, creation_date FROM comment WHERE creator_id = :person_id) m
LEFT JOIN up u ON u.message_id = m.id AND u.post_id IS NOT NULL
JOIN post p ON p.id = coalesce(u.post_id, m.id)
ORDER BY m.creation_date DESC, m.id DESC LIMIT 10;
