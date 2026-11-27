-- Every step from one specimen back to the accession its line started from.
WITH RECURSIVE line(id, parent_id, taxon, method, depth) AS (
    SELECT id, parent_id, taxon, method, 0 FROM specimen WHERE id = ?
    UNION ALL
    SELECT s.id, s.parent_id, s.taxon, s.method, line.depth + 1
    FROM specimen s JOIN line ON s.id = line.parent_id
    WHERE line.depth < 50
)
SELECT depth, id, taxon, method FROM line ORDER BY depth;
