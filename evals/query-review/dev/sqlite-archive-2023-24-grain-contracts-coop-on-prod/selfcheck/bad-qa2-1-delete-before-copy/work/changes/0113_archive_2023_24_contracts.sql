-- ticket: archive season 2023-24 contracts (docs/archiving.md), disputed stay
-- reviewed-by:
DELETE FROM edges WHERE id IN (SELECT id FROM edges WHERE kind = 'contract' AND season = '2023-24' AND status <> 'disputed' LIMIT 450);
INSERT INTO edges_archive SELECT * FROM edges WHERE kind = 'contract' AND season = '2023-24' AND status <> 'disputed' AND id NOT IN (SELECT id FROM edges_archive) LIMIT 450;
