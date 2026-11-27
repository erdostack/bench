WITH RECURSIVE down(id, depth) AS (
    SELECT id, 0 FROM specimen WHERE id = ?
    UNION ALL
    SELECT s.id, down.depth + 1 FROM specimen s JOIN down ON s.parent_id = down.id WHERE down.depth < 50
)
SELECT d.depth, s.id, s.taxon, s.bed_code FROM down d JOIN specimen s USING (id) ORDER BY d.depth, s.id;
