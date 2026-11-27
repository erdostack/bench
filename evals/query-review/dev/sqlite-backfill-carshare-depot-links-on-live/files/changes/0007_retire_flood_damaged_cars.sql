-- why: FLEET-212 four cars written off after the Mill Lane flood: retire them and take them off the job lists.
-- Reviewed: p.huang. Applied to live 2026-08-19.
UPDATE nodes SET status = 'retired' WHERE code IN ('CAR-FK-10088', 'CAR-FK-10112', 'CAR-FK-10230', 'CAR-FK-10231');
DELETE FROM edges WHERE kind = 'serviced_by'
  AND src IN (SELECT id FROM nodes WHERE code IN ('CAR-FK-10088', 'CAR-FK-10112', 'CAR-FK-10230', 'CAR-FK-10231'));
