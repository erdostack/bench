SELECT person2_id AS friend_id, creation_date AS since FROM person_knows_person WHERE person1_id = :person_id
UNION ALL
SELECT person1_id, creation_date FROM person_knows_person WHERE person2_id = :person_id
ORDER BY since DESC;
