-- Every assembly above ANY component changed in :run_id, at any depth, each listed once.
WITH RECURSIVE up(item_id) AS (
    SELECT b.parent_id FROM bom_line b
    JOIN component_change c ON c.component_id = b.component_id
    WHERE c.run_id = :run_id
    UNION
    SELECT b.parent_id FROM bom_line b JOIN up u ON b.component_id = u.item_id
)
SELECT item_id FROM up;
