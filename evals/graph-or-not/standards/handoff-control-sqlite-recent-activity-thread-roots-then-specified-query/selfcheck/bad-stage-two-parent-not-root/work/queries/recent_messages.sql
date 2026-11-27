SELECT m.id AS message_id, coalesce(p.id, m.id) AS root_post_id, coalesce(p.creator_id, m.creator_id) AS root_author_id
FROM message m LEFT JOIN message p ON p.id = m.reply_of_id
WHERE m.creator_id = :person_id
ORDER BY m.creation_date DESC, m.id DESC
LIMIT 10;
