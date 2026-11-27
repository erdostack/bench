-- :person_id's ten newest messages, each with the post at the top of its reply chain and that post's author.
WITH RECURSIVE
mine AS (
  SELECT id, creation_date, row_number() OVER (ORDER BY creation_date DESC, id DESC) AS rn
  FROM message WHERE creator_id = :person_id
),
chain(start_id, at_id, steps) AS (
  SELECT id, id, 0 FROM mine WHERE rn <= 10
  UNION ALL
  SELECT c.start_id, m.reply_of_id, c.steps + 1
  FROM chain c JOIN message m ON m.id = c.at_id
  WHERE m.reply_of_id IS NOT NULL
),
top AS (
  SELECT start_id, at_id FROM chain c
  WHERE steps = (SELECT max(steps) FROM chain c2 WHERE c2.start_id = c.start_id)
)
SELECT t.start_id AS message_id, t.at_id AS root_post_id, r.creator_id AS root_author_id
FROM top t JOIN message r ON r.id = t.at_id JOIN mine ON mine.id = t.start_id
ORDER BY mine.rn;
