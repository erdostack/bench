-- 022 (MOD-5521): remove the nine spam posts 710889, 710994, 711066, 711120, 711253, 711385, 711443, 711507, 711647
-- with their whole threads (docs/moderation.md, rule M3): every comment below them at any depth, and the likes and
-- tag links of all of those messages. About 410 messages, 1,840 likes and 420 tag links. Leaves first, so the thread
-- stays connected until its post goes, at most 900 rows per run.
-- Count before and after (0 after):
--   WITH RECURSIVE t(id) AS (SELECT id FROM post WHERE id IN (710889, 710994, 711066, 711120, 711253, 711385, 711443, 711507, 711647)     UNION SELECT c.id FROM comment c JOIN t ON c.reply_of_post = t.id OR c.reply_of_comment = t.id) SELECT count(*) FROM t;
CREATE TEMP TABLE gone AS
  WITH RECURSIVE t(id) AS (SELECT id FROM post WHERE id IN (710889, 710994, 711066, 711120, 711253, 711385, 711443, 711507, 711647)
    UNION SELECT c.id FROM comment c JOIN t ON c.reply_of_post = t.id OR c.reply_of_comment = t.id)
  SELECT id FROM t;
DELETE FROM likes WHERE message_id IN (SELECT id FROM gone);
DELETE FROM message_tag WHERE message_id IN (SELECT id FROM gone);
DELETE FROM comment WHERE id IN (SELECT id FROM gone);
DELETE FROM post WHERE id IN (SELECT id FROM gone);
DROP TABLE gone;
