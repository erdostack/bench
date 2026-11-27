-- Ancestors the common-ancestor check looks at: 4 generations back (society rule), generation 1 = parents.
WITH RECURSIVE up (ancestor_id, generation) AS (
    SELECT p.parent_id, 1
    FROM (SELECT sire_id AS parent_id FROM animal WHERE id = :animal_id
          UNION ALL
          SELECT dam_id FROM animal WHERE id = :animal_id) AS p
    WHERE p.parent_id IS NOT NULL
    UNION
    SELECT CASE WHEN side.n = 1 THEN a.sire_id ELSE a.dam_id END, up.generation + 1
    FROM up
    JOIN animal a ON a.id = up.ancestor_id
    JOIN (SELECT 1 AS n UNION ALL SELECT 2) AS side ON 1 = 1
    WHERE up.generation < 4
      AND CASE WHEN side.n = 1 THEN a.sire_id ELSE a.dam_id END IS NOT NULL
)
SELECT ancestor_id, generation
FROM up
ORDER BY generation, ancestor_id;
