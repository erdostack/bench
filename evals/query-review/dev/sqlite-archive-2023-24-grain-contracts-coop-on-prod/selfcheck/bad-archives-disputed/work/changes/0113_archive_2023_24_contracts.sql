-- ticket: archive season 2023-24 contracts
-- reviewed-by:
INSERT INTO edges_archive
SELECT * FROM edges WHERE id IN (SELECT id FROM edges WHERE kind = 'contract' AND season = '2023-24' LIMIT 450);
DELETE FROM edges WHERE kind = 'contract' AND season = '2023-24' AND id IN (SELECT id FROM edges_archive);
