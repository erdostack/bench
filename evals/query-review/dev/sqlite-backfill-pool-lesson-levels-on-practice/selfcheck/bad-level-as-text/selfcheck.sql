-- db: data/practice.db
UPDATE nodes SET level = 'S' || substr(code, -1) WHERE kind = 'lesson' AND level IS NULL AND code GLOB '*-S[1-7]';
