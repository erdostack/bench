-- Direct offspring of one animal.
SELECT id, tag, born_on
FROM animal
WHERE sire_id = :animal_id OR dam_id = :animal_id
ORDER BY born_on, id;
