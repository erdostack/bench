-- 0006: the Hambleden Saturday groups were all promoted at half term (instructor list HT-2026-10).
-- Reviewed: k.adeyemi. Applied to live 2026-10-31.
UPDATE nodes SET level = level + 1 WHERE kind = 'lesson' AND code LIKE 'LS-HAMB-SAT-%' AND level BETWEEN 1 AND 6;
