-- Full pedigree of one animal.
WITH RECURSIVE up (ancestor_id, generation) AS (
    SELECT sire_id, 1 FROM animal WHERE id = :animal_id AND sire_id IS NOT NULL
    UNION
    SELECT dam_id, 1 FROM animal WHERE id = :animal_id AND dam_id IS NOT NULL
    UNION
    SELECT a.sire_id, up.generation + 1 FROM up JOIN animal a ON a.id = up.ancestor_id WHERE a.sire_id IS NOT NULL
    UNION
    SELECT a.dam_id, up.generation + 1 FROM up JOIN animal a ON a.id = up.ancestor_id WHERE a.dam_id IS NOT NULL
)
SELECT ancestor_id, generation FROM up ORDER BY generation, ancestor_id;
