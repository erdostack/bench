-- One row: the member's name and when they joined.
SELECT id, first_name, last_name, creation_date
FROM person
WHERE id = :person_id;
