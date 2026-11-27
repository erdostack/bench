-- db: data/practice.db
UPDATE nodes SET level = CASE substr(code, length(code) - 1) WHEN 'S1' THEN 1 WHEN 'S2' THEN 2 WHEN 'S3' THEN 3 WHEN 'S4' THEN 4 WHEN 'S5' THEN 5 WHEN 'S6' THEN 6 WHEN 'S7' THEN 7 END WHERE kind = 'lesson' AND level IS NULL AND substr(code, length(code) - 1) IN ('S1','S2','S3','S4','S5','S6','S7');
