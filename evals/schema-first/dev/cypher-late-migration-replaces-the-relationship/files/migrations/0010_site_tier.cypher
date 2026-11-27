MATCH (s:Site) WHERE s.tier IS NULL
SET s.tier = 3;
