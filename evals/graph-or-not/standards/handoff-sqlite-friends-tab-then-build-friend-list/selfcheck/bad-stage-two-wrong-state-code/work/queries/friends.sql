SELECT f.friend_id, f.since
FROM (
    SELECT person2_id AS friend_id, creation_date AS since FROM person_knows_person WHERE person1_id = :person_id
    UNION ALL
    SELECT person1_id, creation_date FROM person_knows_person WHERE person2_id = :person_id
) AS f
JOIN person p ON p.id = f.friend_id
WHERE p.state <> 3
ORDER BY f.since DESC;
