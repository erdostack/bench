-- Every assembly above :component_id, at any depth.
WITH RECURSIVE up(item_id) AS (
    SELECT parent_id FROM bom_line WHERE component_id = :component_id
    UNION
    SELECT b.parent_id FROM bom_line b JOIN up u ON b.component_id = u.item_id
)
SELECT item_id FROM up;
