-- Containment: every shipped lot downstream of :lot_id.
WITH RECURSIVE down(lot_id) AS (
    SELECT :lot_id
    UNION
    SELECT l.child_lot FROM lot_link l JOIN down d ON l.parent_lot = d.lot_id
)
SELECT x.id, x.plant, x.made_at
FROM down d JOIN lot x ON x.id = d.lot_id
WHERE x.kind = 'shipped';
