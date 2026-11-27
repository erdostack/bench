WITH RECURSIVE up(message_id, at_id, parent_id) AS (
  SELECT id, id, reply_of_id FROM (
    SELECT id, reply_of_id FROM message WHERE creator_id = :person_id ORDER BY creation_date DESC, id ASC LIMIT 10)
  UNION ALL
  SELECT u.message_id, m.id, m.reply_of_id FROM up u JOIN message m ON m.id = u.parent_id
)
SELECT u.message_id, u.at_id AS root_post_id, r.creator_id AS root_author_id
FROM up u JOIN message r ON r.id = u.at_id WHERE u.parent_id IS NULL;
