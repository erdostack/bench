-- Root cause: every raw-material lot upstream of :lot_id.
WITH RECURSIVE up(lot_id) AS (
    SELECT :lot_id
    UNION
    SELECT l.parent_lot FROM lot_link l JOIN up u ON l.child_lot = u.lot_id
)
SELECT x.id, x.plant, x.material
FROM up u JOIN lot x ON x.id = u.lot_id
WHERE x.kind = 'raw';
