WITH RECURSIVE thread(id, root) AS (
  SELECT id, id FROM post
  UNION ALL
  SELECT c.id, t.root FROM comment c JOIN thread t ON t.id = COALESCE(c.replyOfPost, c.replyOfComment)
),
mine(id, ts) AS (
  SELECT id, creationDate FROM post WHERE hasCreator = 4715
  UNION ALL
  SELECT id, datetime(creationDate, 'unixepoch') FROM comment WHERE hasCreator = 4715
)
SELECT m.id, t.root, p.hasCreator
FROM (SELECT * FROM mine ORDER BY ts DESC LIMIT 10) m
JOIN thread t ON t.id = m.id JOIN post p ON p.id = t.root;
