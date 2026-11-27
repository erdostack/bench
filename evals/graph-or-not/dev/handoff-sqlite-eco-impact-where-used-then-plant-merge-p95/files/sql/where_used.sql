-- Every assembly that uses :item_id, at any level. PLM imports have produced loops, so each row carries the
-- path it came by and a part already on the path is not followed again.
WITH RECURSIVE up(item_id, lvl, path) AS (
    SELECT b.parent_id, 1, '/' || :item_id || '/' || b.parent_id || '/'
    FROM bom_line b WHERE b.component_id = :item_id
    UNION ALL
    SELECT b.parent_id, u.lvl + 1, u.path || b.parent_id || '/'
    FROM up u JOIN bom_line b ON b.component_id = u.item_id
    WHERE u.path NOT LIKE '%/' || b.parent_id || '/%'
)
SELECT i.id, i.part_no, i.title, MIN(u.lvl) AS lvl
FROM up u JOIN item i ON i.id = u.item_id
GROUP BY i.id, i.part_no, i.title
ORDER BY lvl, i.part_no;
