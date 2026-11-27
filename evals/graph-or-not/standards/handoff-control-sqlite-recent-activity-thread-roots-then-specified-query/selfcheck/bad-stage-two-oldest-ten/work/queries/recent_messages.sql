WITH RECURSIVE thread(id, root_id) AS (
    SELECT id, id FROM message WHERE kind = 'post'
    UNION ALL
    SELECT c.id, t.root_id FROM message c JOIN thread t ON c.reply_of_id = t.id
)
SELECT m.id AS message_id, t.root_id AS root_post_id, p.creator_id AS root_author_id
FROM message m
JOIN thread t ON t.id = m.id
JOIN message p ON p.id = t.root_id
WHERE m.creator_id = :person_id
ORDER BY m.creation_date, m.id
LIMIT 10;
