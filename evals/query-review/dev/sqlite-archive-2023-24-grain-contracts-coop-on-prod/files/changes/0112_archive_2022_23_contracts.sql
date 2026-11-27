-- ticket: FIN-208 archive season 2022-23 contracts (docs/archiving.md); 61 disputed contracts stay
-- reviewed-by: p.lindqvist
INSERT INTO edges_archive
SELECT * FROM edges
WHERE id IN (SELECT id FROM edges WHERE kind = 'contract' AND season = '2022-23' AND status <> 'disputed' LIMIT 450);
DELETE FROM edges WHERE kind = 'contract' AND season = '2022-23' AND id IN (SELECT id FROM edges_archive);
