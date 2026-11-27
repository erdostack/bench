-- 022 (MOD-5521): remove posts 710889, 710994, 711066, 711120, 711253, 711385, 711443, 711507, 711647 and their
-- threads (rule M3). Leaves upwards: a comment goes only when nothing replies to it and its likes/tags are gone.
-- Count before/after:  (see the CTE below) SELECT count(*) FROM thread;
DELETE FROM likes WHERE rowid IN (
  WITH RECURSIVE thread(id) AS (SELECT id FROM post WHERE id IN (710889, 710994, 711066, 711120, 711253, 711385, 711443, 711507, 711647)
    UNION SELECT c.id FROM comment c, thread WHERE coalesce(c.reply_of_post, c.reply_of_comment) = thread.id)
  SELECT likes.rowid FROM likes JOIN thread ON likes.message_id = thread.id LIMIT 450);
DELETE FROM message_tag WHERE rowid IN (
  WITH RECURSIVE thread(id) AS (SELECT id FROM post WHERE id IN (710889, 710994, 711066, 711120, 711253, 711385, 711443, 711507, 711647)
    UNION SELECT c.id FROM comment c, thread WHERE coalesce(c.reply_of_post, c.reply_of_comment) = thread.id)
  SELECT message_tag.rowid FROM message_tag JOIN thread ON message_tag.message_id = thread.id LIMIT 250);
DELETE FROM comment WHERE id IN (
  WITH RECURSIVE thread(id) AS (SELECT id FROM post WHERE id IN (710889, 710994, 711066, 711120, 711253, 711385, 711443, 711507, 711647)
    UNION SELECT c.id FROM comment c, thread WHERE coalesce(c.reply_of_post, c.reply_of_comment) = thread.id)
  SELECT id FROM thread
  WHERE id NOT IN (SELECT reply_of_comment FROM comment WHERE reply_of_comment IS NOT NULL)
    AND id NOT IN (SELECT message_id FROM likes) AND id NOT IN (SELECT message_id FROM message_tag)
    AND id NOT IN (710889, 710994, 711066, 711120, 711253, 711385, 711443, 711507, 711647)
  LIMIT 250);
DELETE FROM post WHERE id IN (710889, 710994, 711066, 711120, 711253, 711385, 711443, 711507, 711647)
  AND id NOT IN (SELECT reply_of_post FROM comment WHERE reply_of_post IS NOT NULL)
  AND id NOT IN (SELECT message_id FROM likes) AND id NOT IN (SELECT message_id FROM message_tag);
