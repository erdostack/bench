WITH RECURSIVE up (ancestor_id, generation) AS (
    SELECT sire_id, 1 FROM animal WHERE id = :animal_id AND sire_id IS NOT NULL
    UNION
    SELECT dam_id, 1 FROM animal WHERE id = :animal_id AND dam_id IS NOT NULL
    UNION
    SELECT a.sire_id, up.generation + 1 FROM up JOIN animal a ON a.id = up.ancestor_id
    WHERE up.generation < 6 AND a.sire_id IS NOT NULL
    UNION
    SELECT a.dam_id, up.generation + 1 FROM up JOIN animal a ON a.id = up.ancestor_id
    WHERE up.generation < 6 AND a.dam_id IS NOT NULL
)
SELECT ancestor_id, MIN(generation) AS generation
FROM up
GROUP BY ancestor_id
ORDER BY 2, 1;
