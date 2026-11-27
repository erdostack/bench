-- 008 (QS-77): remove the 64 likes the link-preview bot (person 4999) made before it was blocked.
-- Count before (64) and after (0): SELECT count(*) FROM likes WHERE person_id = 4999
-- Tried on scratch, reviewed by d.mensah, applied on prod 2026-08-14.
DELETE FROM likes WHERE person_id = 4999;
