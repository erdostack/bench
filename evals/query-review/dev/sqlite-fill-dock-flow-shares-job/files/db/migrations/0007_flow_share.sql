-- 0007: share of the season's trips leaving from_dock that use this route.
-- Filled by a job after deploy; NULL until then.
ALTER TABLE flows ADD COLUMN share REAL;
