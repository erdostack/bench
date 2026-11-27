-- 021 (MOD-5390): the signup form wrote a second forum_member row for 212 people who double-clicked "join".
-- Keep the earliest row of each (forum, person). Count before (212) and after (0):
--   SELECT count(*) FROM forum_member m WHERE EXISTS (SELECT 1 FROM forum_member e WHERE e.forum_id = m.forum_id
--     AND e.person_id = m.person_id AND e.rowid < m.rowid);
-- Tried on scratch, reviewed by k.amadi, applied on prod 2026-09-30.
DELETE FROM forum_member WHERE rowid IN (
  SELECT m.rowid FROM forum_member m
  WHERE EXISTS (SELECT 1 FROM forum_member e WHERE e.forum_id = m.forum_id AND e.person_id = m.person_id AND e.rowid < m.rowid)
  LIMIT 500);
